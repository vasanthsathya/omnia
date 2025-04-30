Telemetry and visualizations
==============================

The telemetry feature in Omnia allows you to set up a telemetry service that collects telemetry data from the eligible iDRACs in the cluster. It also facilitates the installation of `Grafana <https://grafana.com/>`_ and `Loki <https://grafana.com/oss/loki/>`_ as Kubernetes pods.

.. note:: In order to enable telemetry feature in Omnia, ensure to add ``telemetry`` in the ``/opt/omnia/input/project_default/software_config.json``.

Prerequisites
---------------

To initiate telemetry support, fill out the following parameters in ``input/telemetry_config.yml``:

.. csv-table:: Parameters
   :file: ../Tables/telemetry_config.csv
   :header-rows: 1
   :keepspace:

.. [1] Boolean values does not need double or single quotes.

.. note:: The ``input/telemetry_config.yml`` file is encrypted during the execution of ``omnia.yml`` playbook. Use the below command to decrypt and edit the encrypted input files:
    ::
        ansible-vault edit telemetry_config.yml --vault-password-file .telemetry_vault_key

Playbook execution
-------------------

Once the cluster nodes have been provisioned using the ``discovery_provision.yml`` playbook, you can initiate telemetry service on the cluster using the ``omnia.yml`` or the ``telemetry.yml`` playbook. To invoke the playbooks, use the below commands:

::
    
    ansible-playbook omnia.yml -i <inventory_filepath>

::

    ansible-playbook telemetry.yml -i <inventory_filepath>

.. note::

    * To run the ``telemetry.yml`` playbook independently from the ``omnia.yml`` playbook on nodes with **Intel Gaudi** accelerators, first execute the ``performance_profile.yml`` playbook. Once that’s done, you can run the ``telemetry.yml`` playbook separately.

    * Depending on the type of telemetry initiated, include the following possible groups in the inventory:

        * omnia_telemetry: ``slurm_control_node``, ``slurm_node``, ``login``, ``kube_control_plane``, ``kube_node``, ``etcd``, ``auth_server``

        * idrac_telemetry: ``idrac``

        * k8s_telemetry on Prometheus: ``kube_control_plane``, ``kube_node``, ``etcd``

    * To take a local backup of the telemetry data stored in timescaleDB, use the `timescaledb utility <../Utils/timescaledb_utility.html>`_.

    * After the inventory is up and running, you can use the ``add_idrac_node.yml`` playbook to add new iDRAC nodes for ``idrac_telemetry`` acquisition. To execute the playbook, execute the following command:
        
        ::

            ansible-playbook add_idrac_node.yml -i <inventory_filepath>

Modifying telemetry data collection
-------------------------------------

* To modify how data is collected from the cluster nodes, update the required parameter in ``omnia/input/telemetry_config.yml`` and re-run the ``telemetry.yml`` playbook. Use the below table as reference:

    +--------------------------------------+---------------------------------------------------------------------------------------------------------------------------+
    | Parameters                           | Details                                                                                                                   |
    +======================================+===========================================================================================================================+
    | ``omnia_telemetry_support``          | * **Type**: boolean                                                                                                       |
    |                                      | * If value is set to ``false``, telemetry data collection will be stopped for all nodes mentioned in the inventory file.  |
    |                                      | * If value is set to ``true``, telemetry data collection will be restarted for all nodes mentioned in the inventory file. |
    +--------------------------------------+---------------------------------------------------------------------------------------------------------------------------+

* To start or stop the collection of regular metrics, health check metrics, or GPU metrics, update the values of ``collect_regular_metrics``, ``collect_health_check_metrics``, or ``collect_gpu_metrics``. For a list of all metrics collected, `click here <TelemetryMetrics.html>`_.
 
.. note::
    * Currently, changing the ``grafana_username`` and ``grafana_password`` values is not supported via ``telemetry.yml``.
    * The passed inventory should have an iDRAC group, if ``idrac_telemetry_support`` is true.
    * If ``omnia_telemetry_support`` is true, then the inventory should have OIM and cluster node groups (as specified in the sample files) along with optional login group.
    * If a subsequent run of ``telemetry.yml`` fails, the ``telemetry_config.yml`` file will be unencrypted.

Access the Grafana UI
-------------------------

**Prerequisite**

``visualisation_support`` should be set to ``true`` during ``telemetry.yml`` or ``omnia.yml`` playbook execution.

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


View telemetry data in Grafana
---------------------------------

    1. Login to the Grafana UI by connecting to the cluster IP of grafana service obtained above via port 5000. Example: ``http://xx.xx.xx.xx:5000/login``

    2. In the Explore page, select **telemetry-postgres**.

    .. image:: ../images/Grafana_Telemetry_PostGRES.png
        :width: 600px

    3. The query builder allows you to create SQL commands that can be used to query the ``omnia_telemetry.metrics`` table. Filter the data required using the following fields:

        * **id**: The name of the metric.
        * **context**: The type of metric being collected (Regular Metric, Health Check Metric and GPU metric).
        * **label**: A combined field listing the **id** and **context** row values.
        * **value**: The value of the metric at the given timestamp.
        * **unit**: The unit measure of the metric (eg: Seconds, kb, percent, etc.)
        * **system**: The service tag of the cluster node.
        * **hostname**: The hostname of the cluster node.
        * **time**: The timestamp at which the metric was polled from the cluster node.

    The below image shows a sample of **iDRAC telemetry data in Grafana**

    .. image:: ../images/idractelemetry.png
        :width: 600px

.. note:: If you are more comfortable using SQL queries over the query builder, click on **Edit SQL** to directly provide your query. Optionally, the data returned from a query can be viewed as a graph.

Visualizations
----------------

When ``idrac_telemetry_support`` and ``visualisation_support`` is set to ``true``, Parallel Coordinate graphs in Grafana can be used to view system statistics.

.. toctree::
    Visualizations/index
    TelemetryMetrics
    MetricInfo
    TimescaleDB
    Prometheus_k8s
    Gaudi_metrics




