============================
Troubleshooting guide
============================

Troubleshooting Kubeadm
=========================

For a complete guide to troubleshooting kubeadm, `click here. <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/>`_

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


Checking pod status from the OIM
=====================================
   
   * Use this command to get a list of all available pods: ``kubectl get pods -A``
   * Check the status of any specific pod by running: ``kubectl describe pod <pod name> -n <namespace name>``


Troubleshooting image download failures during ``local_repo.yml`` playbook execution
========================================================================================

If you encounter image download failures while executing ``local_repo.yml``, do the following to resolve the issue:

    1. Check if docker pull limit has been reached by manually trying to download an image. Provide docker credentials in ``provision_config_credentials.yml`` and re-run ``local_repo.yml`` playbook. Else execute ``nerdctl login`` manually.

    2. Run the following command:

            ::

                systemctl status nerdctl-registry

       Expected output:

            .. image:: ../images/image_failure_output_s2.png


       If you don't get the expected output as shown above, run:

            ::

                systemctl restart nerdctl-registry

    3. Run the following command:

            ::

                nerdctl ps -a | grep omnia-registry

        Expected output:

            .. image:: ../images/image_failure_output_s3.png


        If you don't get the expected output as shown above, run:

            ::

                systemctl restart nerdctl-registry

    4. Run the following command:

            ::

                curl -k https://<OIM_hostname>:5001/v2/_catalog

        Expected outputs:

        a. .. image:: ../images/image_failure_output_s4.png
        b. Empty list

        If you don't get the expected output as shown above, do the following:

            a. Restart the OIM and check curl command output again.
            b. Re-run ``local_repo.yml``.

    5. Run the following command:

            ::

                openssl s_client -showcerts -connect <OIM_hostname>:5001

        Expected output:

        .. image:: ../images/image_failure_output_s5.png

        * Verify that the certificate is valid and ``CN=private_registry``.
        * Certificate shown by this command output should be the same as output present at ``/etc/containerd/certs.d/<OIM_hostname>5001/ca.crt``.

        If no certificate is visible on screen, run the following command:

            ::

                    systemctl restart nerdctl-registry


Troubleshooting task failures during ``omnia.yml`` playbook execution
========================================================================

If any task fails for a host listed in the inventory during the execution of the ``omnia.yml`` playbook, it can cause a cascading effect, resulting in the failure of subsequent tasks in the playbook.

**Resolution**: In such cases, you should begin troubleshooting from the initial point of failure — the first task that encountered an error.