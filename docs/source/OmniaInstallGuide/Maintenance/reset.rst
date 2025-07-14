Soft reset the cluster
=======================

Use this playbook to stop and remove all Slurm services from the cluster nodes.

.. warning:: This action will destroy the existing Slurm cluster.

.. note::
    * All target nodes should be drained before executing the playbook. If a job is running on any target nodes, the playbook may timeout while waiting for the node state to change.
    * When running ``reset_cluster_configuration.yml``, ensure that the ``input/storage_config.yml`` and ``input/omnia_config.yml`` have not been edited since ``omnia.yml`` was run.

**Configurations performed by the playbook**

    * The Slurm configuration will be reset on the ``slurm_control_node``, as defined in the inventory file.
    * All services related to Slurm are stopped and removed.

**To run the playbook**

Run the playbook using the following commands: ::

        cd utils
        ansible-playbook reset_cluster_configuration.yml -i inventory

* To specify only Slurm clusters while running the playbook, use the tags ``slurm_cluster``: ::

    ansible-playbook reset_cluster_configuration.yml -i inventory --tags slurm_cluster
    
* To skip confirmation while running the playbook, use ``ansible-playbook reset_cluster_configuration.yml -i inventory --extra-vars skip_confirmation=yes`` or ``ansible-playbook reset_cluster_configuration.yml -i inventory -e  skip_confirmation=yes``.

The inventory file passed for ``reset_cluster_configuration.yml`` should follow the below format. ::

        #Batch Scheduler: Slurm

        [slurm_control_node]

        10.5.1.101

        [slurm_node]

        10.5.1.103

        10.5.1.104

        [login]

        10.5.1.105


        #General Cluster Storage

        [auth_server]

        10.5.1.106
