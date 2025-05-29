Role based additional software installation
============================================

To install multiple packages on cluster nodes in a bulk operation, the ``software_update.yml`` playbook can be leveraged.

Prerequisites
---------------

* Download the required packages to the Pulp container using the ``local_repo.yml`` playbook.
* Ensure that the target cluster nodes are in ``booted`` state.
* Add the following entry under the ``softwares`` section in ``/opt/omnia/input/project_default/software_config.json``: ::
    
    "softwares": [ 
               
               {“name”: “additional_software”} 
            
            ]

Steps
-------

1. Create a ``additional_software.json`` file under ``input/config/<cluster_os_type>/<cluster_os_version>`` directory, with all the additional packages listed. These packages will be installed on the cluster nodes.

2. Provide details about the software installation requirements for each group or role in the ``/opt/omnia/input/project_default/software_config.json`` file. Use the format of subgroups, where each subgroup name is a comma-separated list of group or role names.

    * Specify the **role** in order to install the desired packages on all the nodes linked to a specific role. 
        
        **Example**: In the below example, the packages will be installed on all the nodes linked to the role ``default`` and ``compiler_node``:
        ::

            "additional_software": [
                
                {"name": "default,compiler_node"}

            ]

    * Specify the **group names** in order to install the desired packages on all the nodes linked to specific groups. 
        
        **Example**: In the below example, the packages will be installed on all the nodes linked to ``grp1`` and ``grp 2``: 
        ::

            "additional_software": [
                
                {"name": "grp1,grp2"}

            ]

    * Specify a combination of **role** and **group names** in order to install the desired packages on a specific group of nodes under a role. 
        
        **Example**: In the below example, the packages will be installed on all the nodes linked to ``grp2`` of the ``default`` role: 
        ::

            "additional_software": [
                
                {"name": "default,grp2"}

            ]

.. note:: If no roles or groups are specified, the packages will be installed on all the nodes.

Input parameters
-----------------

Enter the following parameters in ``input/config/<cluster_os_type>/<cluster_os_version>/additional_software.json``:

.. csv-table:: additional_software.json
    :file: ../Tables/additional_software.csv
    :header-rows: 1
    :keepspace:


Sample of ``additional_software.json``
----------------------------------------

The below provided sample contains all the possible combinations for roles and groups in the ``additional_software.json``:

::

            {
              "additional_software": {
                "cluster": [
                  {
                    "package": "quay.io/jetstack/cert-manager-controller",
                    "type": "image",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },
                  
                  {
                    "package": "quay.io/jetstack/cert-manager-webhook",
                    "type": "image",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },
                  
                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },
                ]
              
              "default, compiler_node": {
                "cluster": [
                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },

                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  }
                ]
              
              "grp1,grp3": {
                "cluster": [
                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },

                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },
                ]
              
              "default,grp2": {
                "cluster": [
                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  },

                  {
                    "package": "nfs-common",
                    "type": "deb",
                    "url": "",
                    "path": ""
                    "reboot_required":
                  }

                ]
              
              }

            }


Playbook execution
--------------------

Run the playbook using the following command: ::

    cd utils/software_update
    ansible-playbook software_update.yml

