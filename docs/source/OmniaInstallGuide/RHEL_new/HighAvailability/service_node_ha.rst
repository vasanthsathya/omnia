High Availability (HA) for the Service Node
=====================================================

In a large HPC cluster deployed by Omnia, service nodes are used to balance the load on the OIM. Each service node is responsible for discovering and provisioning a set of compute nodes. 
For such scenarios, in order to maintain uninterrupted cluster experience, Omnia provides an option to enable high availability for the service nodes. HA Service nodes are brought online when their associated Service nodes fail.

Prerequisites
--------------

* To enable and configure the HA for OIM, fill up the necessary parameters in the ``high_availability_config.yml`` config file present in the ``/opt/omnia/input/project_default/`` directory. Refer the following table while doing so:

    .. csv-table:: Parameters for Service Node HA
        :file: ../../../Tables/sn_ha.csv
        :header-rows: 1
        :keepspace:

Playbook execution
-------------------

Once the details are provided to the input files, HA service nodes can be discovered during the cluster discovery and provision process using the below command:

::

    ansible-playbook discovery_provision.yml --tags "management_layer"


Sample
-------

::

    Service_node_ha: 

        enable_servicenode_ha: false 

          Service_nodes: 

         	- virtual_ip_address: “10.5.0.11” 

                Active_node: “D636R10” 

                passive_node:  

                  - Node_details: “D636R11”

            - virtual_ip_address: “10.5.0.12” 

                Active_node: “D636R12” 

                passive_node:  

                  - Node_details: “D636R13” 

            - virtual_ip_address: “10.5.0.13” 

                Active_node: “D636R14” 

                passive_node:  

                  - Node_details: “D636R15”