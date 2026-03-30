#!/bin/bash

set -eo pipefail

mkdir -p /etc/ansible
cp ansible.cfg /etc/ansible/ansible.cfg

cp inventory.py /etc/ansible/inventory.py
chmod +x /etc/ansible/inventory.py