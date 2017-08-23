# ansible-openstack
Ansible Playbook to manage servers on a pre-existent OpenStack cloud

The recipes contain an ```openstack``` role that creates and deletes virtual machines on a OpenStack platform.
This is reached with the OpenStack API and Ansible OS Modules (os_server, os_port, os_volume) and needs the OpenStack Client to perform the operations on OpenStack platform.
In our production environment, we decided to install the OpenStack Client on the "```localhost```" machine and use inventory ```group_vars``` to provide the needed variables.

## Requirements

* [Ansible](https://www.ansible.com/) - Tested with Ansible v2.3.1.0
* [OpenStack Client](https://docs.openstack.org/user-guide/common/cli-install-openstack-command-line-clients.html)

## Simple flow to Instance new virtual Machine

1. Be sure that the OpenStack Client is installed and works when you'll run this Playbook (on localhost in our case)

2. Become ROOT:
   * ```sudo su -```

3. Retrieve GIT repository of the project:
   * ```apt-get install git```
   * ```cd /opt ; git clone https://github.com/malavolti/ansible-openstack.git```

4. Create your ```.vault_pass.txt``` that contains the encryption password (this is needed ONLY when you use Ansible Vault):
   * ```cd /opt/ansible-openstack```
   * ```openssl rand -base64 64 > .vault_pass.txt```

5. Create the Openstack Client configuration file by copying/filling the templates:
    * ```/opt/ansible-openstack/#_environment_#/group_vars/all.yml-template```
    * ```/opt/ansible-openstack/#_environment_#/group_vars/openstack-client.yml-template```

   into proper ```/opt/ansible-openstack/#_environment_#/group_vars/all.yml``` and ```/opt/ansible-openstack/#_environment_#/group_vars/openstack-client.yml``` files.
   These files will provide to Ansible all variables needed to instance (or delete) virtual machines on Openstack Cloud by its CLI.

6. Encrypt the Openstack configuration files with Ansible Vault (Optional: this is needed ONLY when you need Ansible Vault):
   * ```cd /opt/ansible-openstack```
   * ```ansible-vault encrypt inventories/#_environment_#/group_vars/all.yml --vault-password-file .vault_pass.txt```
   * ```ansible-vault encrypt inventories/#_environment_#/group_vars/openstack-client.yml --vault-password-file .vault_pass.txt```

7. Execute this command to run Ansible on develoment inventory and to instance new virtual machine:
   * ```ansible-playbook site.yml -i inventories/development/development.ini --vault-password-file .vault_pass.txt```


## Useful Commands

```
--- development.ini ---
[openstack-client]
localhost
-----------------------
```

1. Test that the connection with the server(s) is working:
   * ```ansible all -m ping -i /opt/ansible-openstack/inventories/#_environment_#/#_environment_#.ini -u debian```
   ("```debian```" is the user used to perform the SSH connection with the client to synchronize)

2. Get the facts from the server(s):
   * ```ansible GROUP_NAME -m setup -i /opt/ansible-openstack/inventories/#_environment_#/#_environment_#.ini -u debian```

   Examples:
      * without encrypted files:
         ```ansible GROUP_NAME -m setup -i /opt/ansible-openstack/inventories/#_environment_#/#_environment_#.ini -u debian```
      * with encrypted files:
         ```ansible GROUP_NAME -m setup -i /opt/ansible-openstack/inventories/#_environment_#/#_environment_#.ini -u debian --vault-password-file .vault_pass.txt```

      ("```.vault_pass.txt```" is the file you have created that contains the encryption password)

3. Encrypt files:
   * ```ansible-vault encrypt inventories/#_environment_#/group_vars/all.yml --vault-password-file .vault_pass.txt```
   * ```ansible-vault encrypt inventories/#_environment_#/group_vars/openstack-client.yml --vault-password-file .vault_pass.txt```

4. Decrypt Encrypted files:
   * ```ansible-vault decrypt inventories/#_environment_#/group_vars/all.yml --vault-password-file .vault_pass.txt```
   * ```ansible-vault decrypt inventories/#_environment_#/group_vars/openstack-client.yml --vault-password-file .vault_pass.txt```

5. View Encrypted files:
   * ```ansible-vault view inventories/#_environment_#/group_vars/all.yml --vault-password-file .vault_pass.txt```
   * ```ansible-vault view inventories/#_environment_#/group_vars/openstack-client.yml --vault-password-file .vault_pass.txt```

## Authors

#### Original Author and Development Lead

* Marco Malavolti (marco.malavolti@gmail.com)
