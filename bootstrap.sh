#!/bin/bash

set -o pipefail

cp ansible.cfg /etc/ansible/ansible.cfg

cp inventory.py /etc/ansible/inventory.py
chmod +x ~/.inventory.py

mkdir -p /usr/share/ansible/plugins/modules
cp -rf module_plugins/* /usr/share/ansible/plugins/modules/

mkdir -p /usr/share/ansible/plugins/action
cp -rf action_plugins/* /usr/share/ansible/plugins/action/