#!/usr/bin/env python3

import os
import sys
import argparse
import json
import base64
import random
from kubernetes import client, config
from kubernetes.config import ConfigException

"""
Teknoir Notebook custom dynamic inventory script for Ansible, in Python.
"""


class TeknoirInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.teknoir_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.teknoir_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory, indent=4, sort_keys=True));

    def decode(self, s):
        return base64.b64decode(s.encode('utf-8')).decode('utf-8')

    def _start_reverse_tunnel(self, custom_api, namespace, name):
        # display.v(f"Start reverse tunnel", host=self.inventory)
        port = str(random.randint(1024, 64511))
        device_patch = {
            "spec": {
                "keys": {
                    "data": {
                        "tunnel": base64.b64encode(port.encode('utf-8')).decode('utf-8')
                    }
                }
            }
        }
        custom_api.patch_namespaced_custom_object("kubeflow.org",
                                                  "v1beta1",
                                                  namespace,
                                                  "devices",
                                                  name,
                                                  device_patch)
        self.tunnel_opened = True
        return port

    def teknoir_inventory(self):
        namespace = os.getenv('NAMESPACE', "namespace does not exist")
        config.load_incluster_config()
        custom_api = client.CustomObjectsApi()
        devices = custom_api.list_namespaced_custom_object(group="kubeflow.org",
                                                           version="v1",
                                                           plural="devices",
                                                           namespace=namespace)

        inventory = {
            '_meta': {
                'hostvars': {}
            }
        }
        ssh_port = 2200
        for device in devices['items']:
            ansible_group = device["metadata"]["namespace"].replace('-', '_')
            current_work_dir = os.getcwd()
            path = f'{current_work_dir}/inv/{ansible_group}/'
            hostname = f'{device["metadata"]["name"]}'

            if ansible_group not in inventory:
                inventory[ansible_group] = {
                    'hosts': [],
                    'vars': {}
                }
                os.makedirs(path, exist_ok=True)
            inventory[ansible_group]['hosts'].append(hostname)

            for label, value in device["metadata"]["labels"].items():
                label = label.replace('-', '_')
                value = value.replace('-', '_')
                additional_group = f'{label}_{value}'
                if additional_group not in inventory:
                    inventory[additional_group] = {
                        'hosts': [],
                        'vars': {}
                    }
                inventory[additional_group]['hosts'].append(hostname)

            private_key_file = f'{path}{device["metadata"]["name"]}.pem'
            with open(private_key_file, 'w') as outfile:
                outfile.write(self.decode(device['spec']['keys']['data']['rsa_private']))
            os.chmod(private_key_file, 0o600)

            tunnel_port = self.decode(device['spec']['keys']['data']['tunnel'])
            if not tunnel_port.isdigit():
                tunnel_port = self._start_reverse_tunnel(custom_api, device["metadata"]["namespace"],
                                                         device["metadata"]["name"])


            inventory['_meta']['hostvars'][hostname] = {
                'ansible_connection': 'ssh',
                'ansible_port': tunnel_port,
                'ansible_host': 'localhost',
                'ansible_user': self.decode(device['spec']['keys']['data']['username']),
                'ansible_sudo_pass': self.decode(device['spec']['keys']['data']['userpassword']),
                'ansible_become': 'yes',
                'ansible_become_user': 'root',
                'ansible_become_pass': self.decode(device['spec']['keys']['data']['userpassword']),
                'ansible_ssh_private_key_file': private_key_file,
                'ansible_python_interpreter': '/usr/bin/python3',
                'ansible_ssh_retries': 20,
                'ansible_kubectl_namespace': device["metadata"]["namespace"],
                'ansible_teknoir_device': device['metadata']['name']
            }
            ssh_port = ssh_port + 1
        return inventory

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


# Get the inventory.
TeknoirInventory()
