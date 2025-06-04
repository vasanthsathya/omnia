Access the Grafana UI
========================

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