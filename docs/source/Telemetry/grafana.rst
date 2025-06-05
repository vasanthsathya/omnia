Access the Grafana UI
========================

**Prerequisite**

``visualization_support`` should be set to ``true`` during ``prepare_oim.yml`` playbook execution. For more information, `click here <../OmniaInstallGuide/RHEL_new/prepare_oim.html#telemetry-config-yml>`_.

**Steps**

    1. Log in to the Grafana UI via port 5000. Enter the below URL into the browser's address bar: ::
        
        http://localhost:5000/login


        .. image:: ../images/Grafana_login.png
            :width: 600px


    3. Enter the ``grafana_username`` and ``grafana_password`` as mentioned previously in the ``/opt/omnia/input/project_default/omnia_config_credentials.yml`` input file.


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

    1. Log in to the Grafana UI via port 5000. Enter the below URL into the browser's address bar: ::
        
        http://localhost:5000/login

    2. In the Explore page, select **oim-node-loki**.

        .. image:: ../images/Grafana_ControlPlaneLoki.png
            :width: 600px

    3. The log browser allows you to filter logs by job, node, and/or user.

    Example: ::

        (job="cluster deployment logs") |= "nodename"
        (job="compute log messages") |= "nodename" |="node_username"