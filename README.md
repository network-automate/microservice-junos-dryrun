# Microservice to push configuration to Junos device.

## Description

This microservice provides mechanism to render a candidate configuration file against junos device, save rendered configuration and get the difference between running and candidate.

__Docker image:__ [`jnprautomate/junos-dryrun`](https://hub.docker.com/r/jnprautomate/junos-dryrun)

__Basic usage__


```shell
# Pull image from docker
% docker pull jnprautomate/junos-dryrun

# Create folder structure
% mkdir {inputs,configs,diffs}

# make inventory for ansible
vim inputs/inventory.ini

% docker run -it --rm \
	-v ${PWD}/inputs:/inventory \
	-v ${PWD}/diffs:/outputs \
	-v ${PWD}/configs:/config \
	jnprautomate/junos-dryrun:latest
```

## Data management:

__Inputs__

- Ansible Inventory file (inventory.ini) with following elements:
    - `ansible_host`: IP of the device
    - `netconf_port`: netconf port uses to connect to devices (default is 830)
    - `ansible_ssh_private_key`: Private key to use to authenticate against devices (Optional)
    - `ansible_ssh_user`: Username to use for the connection
    - `ansible_ssh_pass`: Password to use for the connection (Optional if private key is configured)
- `commit_mode`: define how configuration management is. done: `merge` or `replace` (optional)
- Configuration folder where all configuration files are stored with this syntax: `{{inventory_hostname}}.conf`

__Outputs__

- `outputs`: folder where both diff and rendered configurations take place.

__Volumes to mount__

- `inventory`: Folder where inventory file is located
- `config`: Folder where all the configuration files are located
- `outputs`: Optional folder to get access to all diff when configuration are committed.

## Output example

Below is an example of how to use this container

* Build your inventory

```shell
evpn-microservice ᐅ cat inventory/inventory.ini

[demo]
demo-qfx10k2-14    ansible_host=172.25.90.67
demo-qfx10k2-15    ansible_host=172.25.90.68

[demo:vars]
netconf_port=830
ansible_ssh_user=ansible
ansible_ssh_pass=juniper123
ansible_ssh_private_key = "~/.ssh/id_lab_gsbt"
commit_mode="merge"
```

* Check your configurations to the correct folder:

```shell
evpn-microservice ᐅ tree -L 2
.
├── configs
│   ├── demo-qfx10k2-14.conf
│   └── demo-qfx10k2-15.conf
├── diffs
└── inputs
    └── inventory.ini
```

* Run service within docker container

```shell
evpn-microservice ᐅ docker run -it --rm \
        -v ${PWD}/inputs:/inventory \
        -v ${PWD}/diffs:/outputs \
        -v ${PWD}/configs:/config \
        jnprautomation/dryrun:latest

Deploy configuration to Junos devices
  > Check inventory file
  > Inventory file found (inputs/inventory.ini)
  > Deploy configurations to devices

PLAY [Deploy configuration] *******************************************************************************************

TASK [include_vars] ***************************************************************************************************
ok: [demo-qfx10k2-14]
ok: [demo-qfx10k2-15]

TASK [config-deploy-core : Create output directory for device] ********************************************************
changed: [demo-qfx10k2-15]
changed: [demo-qfx10k2-14]

TASK [config-deploy-core : Push Configuration to devices (commit check)] **********************************************
changed: [demo-qfx10k2-15]
changed: [demo-qfx10k2-14]

TASK [config-deploy-core : Pushing config, doing commit check and downloading candidate config... please wait] ********
changed: [demo-qfx10k2-15]
changed: [demo-qfx10k2-14]

PLAY RECAP ************************************************************************************************************
demo-qfx10k2-14            : ok=4    changed=3    unreachable=0    failed=0
demo-qfx10k2-15            : ok=4    changed=3    unreachable=0    failed=0
```

* Get the result

```shell

evpn-microservice ᐅ tree -L 2
.
├── configs
│   ├── demo-qfx10k2-14.conf
│   └── demo-qfx10k2-15.conf
├── diffs
│   ├── demo-qfx10k2-14
│   │   ├── candidate-rendered-demo-qfx10k2-14.conf
│   │   └── config-diff.log
│   └── demo-qfx10k2-15
│       ├── candidate-rendered-demo-qfx10k2-15.conf
│       └── config-diff.log
└── inputs
    └── inventory.ini

```