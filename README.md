# Teknoir Ansible Notebook Demo
Notebooks runs in namespaces, the scope of devices to control is defined by the namespace. 

## Limitations
* Namespaces become groups, we do not support namespaces with dashes(-).
  * Dashes(-) will be replaced with underscores(_)
* Labels become groups as follows:
  * A label consists of key and value
  * Groups are contructed concatinating key and value separated by underscore(_)
  * I.e. key_value
* The Plugin do not automatically open or close reverse-tunnels

## Requirements
* corkscrew
* rsync

## List devices
```bash
ansible -i inventory.py --list-hosts all
```

## Patch devices
```bash
ansible-playbook -v -i inventory.py playbook.yaml --limit my-device-01,my-device-02
```
