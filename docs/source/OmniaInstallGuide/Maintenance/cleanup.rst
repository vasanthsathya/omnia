OIM cleanup
===============

The ``oim_cleanup.yml`` playbook can be utilized to roll back any configurations made on the OIM. 
It removes containers, log files, and metadata from the OIM node(s), resets firewall ports, and reboots service nodes to prepare the infrastructure for future provisioning tasks. 
Its behavior varies based on the type of cluster configuration: non-hierarchical, hierarchical, and whether High Availability (HA) is enabled or not.

Behavior based on cluster configuration
----------------------------------------

1. **Non-hierarchical, non-HA** configuration

In this setup, when executed from the OIM node, this playbook will:

    * Clean up all containers, log files, and metadata on the OIM node.
    * Update the firewall ports on the OIM node to its default setting.

2. **Hierarchical, non-HA** configuration

In this setup, when executed from the OIM node, this playbook will:

    * Disable the boot option on all service nodes.

    * Reboot all service nodes so that they pause and wait for boot media.

    * Clean up containers, logs, and metadata on the OIM node.

    * Update firewall ports on the OIM node to its default setting.

3. **Hierarchical, HA** configuration

a. **When executed from the Primary OIM node:**

    * Disables boot options on:
          
        i. All service nodes
        ii. The passive OIM node

    * Reboots:

        i. All service nodes
        ii. Passive OIM node

    * Cleans up containers, log files, and metadata from the **primary** OIM node.
    * Updates firewall ports on the **primary** OIM node to its default setting.

b. **When executed from the OIM-HA node:** (previously passive, now active due to failover)

    * Disables boot options on all service nodes (including passive)
    * Reboots all service nodes
    * Cleans up containers, log files, and metadata from **both OIM nodes** (active and passive).
    * Updates firewall ports on **both OIM nodes** (active and passive) to its default setting.

Playbook execution
-------------------

Use the below command to execute the playbook: ::

    cd utils
    ansible-playbook oim_cleanup.yml

.. note:: If any OIM or service node is not in a booted state, **no action** will be taken on that node during playbook execution.

.. note:: After you run the ``oim_cleanup.yml`` playbook, ensure to reboot the OIM node.

.. caution::
    * When re-provisioning your cluster (that is, re-running the ``discovery_provision.yml`` playbook) after a clean-up, ensure to use a different ``admin_nic_subnet`` in ``input/provision_config.yml`` to avoid a conflict with newly assigned servers. Alternatively, disable any OS available in the ``Boot Option Enable/Disable`` section of your BIOS settings (``BIOS Settings`` > ``Boot Settings`` > ``UEFI Boot Settings``) on all target nodes.
    * On subsequent runs of ``discovery_provision.yml``, if users are unable to log into the server, refresh the ssh key manually and retry. ::

        ssh-keygen -R <node IP>