Step 6: Verify the status of Omnia Core Container Service and associated services
=================================================================================
After deploying the Omnai Core Container, you can verify that the Omnia core service and
its dependent services are running correctly.

1. Run the following command to check the status of the OMNIA Core service:

   .. code-block:: bash

      systemctl status omnia_core.service

   This command displays whether the ``omnia_core.service`` is active, inactive,
   or has failed. 

2. To view the complete list of dependent services for the OMNIA target, run:

   .. code-block:: bash

      systemctl list-dependencies omnia.target --all

3. Review the status of the dependent services in the following tree output. 

   .. code-block:: text

      omnia.target
      ● ├─omnia_core.service
      ● ├─network-online.target
      ● │ └─NetworkManager-wait-online.service
      ● ├─kubespray.service
      ● ├─pulp.service
      ● └─openchami.target
      ●   ├─acme-deploy.service
      ●   ├─acme-register.service
      ●   ├─bss-init.service
      ●   ├─bss.service
      ●   ├─cloud-init-server.service
      ●   ├─coresmd.service
      ●   ├─haproxy.service
      ●   ├─hydra-gen-jwks.service
      ●   ├─hydra-migrate.service
      ●   ├─hydra.service
      ●   ├─opaal-idp.service
      ●   ├─opaal.service
      ●   ├─openchami-cert-trust.service
      ●   ├─postgres.service
      ●   ├─smd.service
      ●   └─step-ca.service

   * A **green circle** indicates that the service is running.
   * A **grey circle** indicates that the service is not running.
   * A **circle with a cross** indicates that the service failed to start.

