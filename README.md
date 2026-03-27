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
* rsync

## List devices
```bash
ansible --list-hosts all
```

## Synchronize (rsync) from host to local
```bash
ansible <device_name> -m synchronize -a "src=/path/to/source/dir/ dest=/path/to/local/target/dir/ use_ssh_args=yes mode=pull"
```
_Synchronize does not work with "become"(sudo)_

## Syncronize (rsync) from local to host
```bash
ansible <device_name> -m synchronize -a "src=/path/to/local/source/dir/ dest=/path/to/target/dir/ use_ssh_args=yes"
```
_Synchronize does not work with "become"(sudo)_

## Run playbook examples
Run for one device:
```bash
ansible-playbook -v -i inventory.py playbook.yaml --limit <device_name>
```

## Run for all devices with label:
```bash
ansible-playbook -v -i inventory.py playbook.yaml --limit <label>
```
_Observe how labels are constructed, see Limitations above!_