# Teknoir Ansible Notebook Demo
Notebooks runs in namespaces, the scope of devices to control is defined by the namespace. 

## Limitations
* Namespaces become groups, we do not support namespaces with dashes(-).
  * Dashes(-) will be replaced with underscores(_)
* The Connection Plugin automatically enable tunnels for devices but...
  * does not tear them down after
    
## List devices
```bash
ansible -i inventory.py --list-hosts all
```

## Patch devices
```bash
ansible-playbook -v -i inventory.py playbook.yaml --limit my-device-01,my-device-02
```
