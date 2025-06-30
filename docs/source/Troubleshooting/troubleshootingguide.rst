============================
Troubleshooting guide
============================

Connecting to internal databases
===================================

TimescaleDB
--------------

    * Start a bash session within the timescaledb pod: ``kubectl exec -it pod/timescaledb-0 -n telemetry-and-visualizations -- /bin/bash``
    * Connect to psql using the ``psql -u <postgres_username>`` command.
    * Connect to database using the ``\c telemetry_metrics`` command.

MySQL DB
-----------

    * Start a bash session within the mysqldb pod using the ``kubectl exec -it pod/mysqldb-0 -n telemetry-and-visualizations -- /bin/bash`` command.
    * Connect to mysql using the ``mysql -u <mysqldb_username>`` command and provide password when prompted.
    * Connect to database using the ``USE idrac_telemetrysource_services_db`` command.

Checking and updating encrypted parameters
=============================================

1. Move to the filepath where the parameters are saved (as an example, we will be using ``provision_config_credentials.yml``): ::

        cd /input

2. To view the encrypted parameters: ::

        ansible-vault view provision_config_credentials.yml --vault-password-file .provision_credential_vault_key


3. To edit the encrypted parameters: ::

        ansible-vault edit provision_config_credentials.yml --vault-password-file .provision_credential_vault_key


Checking podman container status from the OIM
===============================================
   
   * Use this command to get a list of all available pods: ``kubectl get pods -A``
   * Check the status of any specific pod by running: ``kubectl describe pod <pod name> -n <namespace name>``


Troubleshooting task failures during ``omnia.yml`` playbook execution
========================================================================

If any task fails for a host listed in the inventory during the execution of the ``omnia.yml`` playbook, it can cause a cascading effect, resulting in the failure of subsequent tasks in the playbook.

**Resolution**: In such cases, you should begin troubleshooting from the initial point of failure — the first task that encountered an error.