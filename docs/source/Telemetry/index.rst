Telemetry and visualizations
==============================

The telemetry feature in Omnia allows you to set up a telemetry service that collects telemetry data from the eligible iDRACs in the cluster. It also facilitates the installation of `Grafana <https://grafana.com/>`_ and `Loki <https://grafana.com/oss/loki/>`_ as Podman containers.

Prerequisites
---------------

To enable telemetry support, set ``idrac_telemetry_support`` to ``true`` and ``idrac_telemetry_collection_type`` to ``prometheus`` in the ``telemetry_config.yml`` file. Then, run the ``prepare_oim.yml`` playbook, which deploys the containers necessary for the telemetry service. For more information, `click here <../OmniaInstallGuide/RHEL_new/prepare_oim.html#telemetry-config-yml>`_.

.. note:: To update the ``bmc_username`` and ``bmc_password`` fields in the ``omnia_config_credentials.yml`` input file for the connected iDRACs, use the command provided below. Do not alter any other fields in the file, as this may lead to unexpected failures. For more information, `click here <../OmniaInstallGuide/RHEL_new/credentials_utility.html>`_.
    ::
        ansible-vault edit omnia_config_credentials.yml --vault-password-file .omnia_config_credentials_key

Playbook execution
-------------------

Once the cluster nodes have been provisioned using the ``discovery_provision.yml`` playbook, you can initiate telemetry service on the cluster using the ``telemetry.yml`` playbook. To invoke the playbooks, use the below commands:

::

    ansible-playbook telemetry.yml

.. note::

    * After ``discovery_provision.yml`` playbook has been executed, an inventory file called ``bmc_group_data.csv`` file is created under the ``/opt/omnia/telemetry/`` directory. This file acts as the default inventory for the ``telemetry.yml`` playbook. If you want to add an external node for ``idrac_telemetry`` acquisition, you can do so by editing the ``bmc_group_data.csv`` file manually and then re-running the ``telemetry.yml`` playbook. Sample: ::

        BMC_IP,GROUP_NAME,PARENT
        10.5.0.101,grp0,ABCD123
        10.5.1.102,grp1,EFGH456
    
    * To run the telemetry services on nodes with **Intel Gaudi** accelerators, first execute the ``performance_profile.yml`` playbook followed by the ``telemetry.yml`` playbook.

    * To take a local backup of the telemetry data stored in timescaleDB, use the `timescaledb utility <../Utils/timescaledb_utility.html>`_.

Access the Grafana UI
-------------------------

**Prerequisite**

``visualization_support`` should be set to ``true`` during ``prepare_oim.yml`` playbook execution. For more information, `click here <../OmniaInstallGuide/RHEL_new/prepare_oim.html#telemetry-config-yml>`_.

**Steps**

    1. Find the IP address of the Grafana service using ``kubectl get svc -n grafana``


        .. image:: ../images/grafanaIP.png
                :width: 600px


    2. Login to the Grafana UI by connecting to the cluster IP of grafana service obtained above via port 5000, that's ``http://xx.xx.xx.xx:5000/login``


        .. image:: ../images/Grafana_login.png
            :width: 600px


    3. Enter the ``grafana_username`` and ``grafana_password`` as mentioned in ``input/telemetry_config.yml``.


        .. image:: ../images/Grafana_Dashboards.png
            :width: 600px


    4. Loki log collections can viewed on the explore section of the grafana UI.


        .. image:: ../images/Grafana_Loki.png
            :width: 600px


    5. Datasources configured by Omnia can be viewed below: 


        .. image:: ../images/GrafanaDatasources.png
            :width: 600px

Filter logs using Loki
-----------------------

    1. Login to the Grafana UI by connecting to the cluster IP of grafana service obtained above via port 5000. That is ``http://xx.xx.xx.xx:5000/login``

    2. In the Explore page, select **control-plane-loki**.

        .. image:: ../images/Grafana_ControlPlaneLoki.png
            :width: 600px

    3. The log browser allows you to filter logs by job, node, and/or user.

    Example: ::

        (job="cluster deployment logs") |= "nodename"
        (job="compute log messages") |= "nodename" |="node_username"

Visualizations
----------------

When ``idrac_telemetry_support`` and ``visualization_support`` is set to ``true``, Parallel Coordinate graphs in Grafana can be used to view system statistics.

.. toctree::
    Visualizations/index
    TimescaleDB
    Prometheus_k8s
    Gaudi_metrics




