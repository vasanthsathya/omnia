High Availability (HA) for the Service Cluster
================================================

Prerequisites
--------------

* Ensure that the passive service nodes have ``service_node`` role assigned to them in the ``/opt/omnia/input/project_default/roles_config.yml`` input file. For more information, `click here <../composable_roles.html>`_.

* Ensure that all the service nodes (active/passive) are connected to the Internet.

* Ensure that the ``local_repo.yml`` playbook has been run successfully at least once. Before running it, verify that the ``opt/omnia/input/project_default/software_config.json`` file contains ``{"name": "service_node"}`` in the ``softwares`` list.

* To enable and configure the HA for Service cluster, fill up the necessary parameters in the ``high_availability_config.yml`` config file present in the ``/opt/omnia/input/project_default/`` directory. Once the config file is updated, run the ``prepare_oim.yml`` playbook.

    .. csv-table:: Parameters for Service Cluster HA
        :file: ../../../Tables/service_cluster_ha.csv
        :header-rows: 1
        :keepspace:

.. note:: 
  
    * Once the ``prepare_oim.yml`` playbook has been executed, any subsequent edits to the ``high_availability_config.yml`` or ``roles_config.yml`` files will not take effect. To apply changes made to these configuration files, you must re-run the ``prepare_oim.yml`` playbook.
    * The virtual IP addresses specified in the ``high_availability_config.yml`` file must be within the same subnet as the admin network.

Playbook execution
-------------------

Once the details have been provided to the input files and the ``prepare_oim.yml`` playbook is executed, passive service nodes can be discovered during the cluster discovery and provision process using the below command:

::

    ansible-playbook discovery_provision.yml --tags "management_layer"

.. note:: Ensure that ``local_repo.yml`` playbook has been executed successfully before provisioning.

Sample
-------

::
    
    service_k8s_cluster_ha:
        - cluster_name: service_cluster
          enable_k8s_ha: false
          virtual_ip_address: ""
          external_loadbalancer_ip: ""
          loadbalancer_port:
          active_node_service_tags: [ABCD123, DEF4567]