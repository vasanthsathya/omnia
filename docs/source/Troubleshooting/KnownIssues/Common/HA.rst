High Availability (HA)
======================

⦾ **In a HA-setup, the xCAT post-installation script fails while switching from an active to passive OIM, during failover scenarios. This halts the OS-provisioning on the compute nodes.**

**Potential Cause**: This issue occurs due to an open defect in xCAT. For more information, `click here <https://github.com/xcat2/xcat-core/issues/7503>`_.

**Resolution**: If this occurs, wait until all containers have fully transitioned and confirm that the ``omnia_pcs`` container is up and running on the passive OIM node. Then, re-run any failed OS provisioning tasks.