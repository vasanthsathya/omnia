High Availability (HA)
======================

⦾ **In a HA-setup, the xCAT post-installation script fails while switching from an active to passive OIM, during failover scenarios. This halts the OS-provisioning on the compute nodes.**

**Potential Cause**: This is due to an open defect on xCAT. For more information, `click here <https://github.com/xcat2/xcat-core/issues/7503>`_.

**Resolution**: Users encountering this issue must re-run any failed installations after the containers have fully transitioned and ``omnia_pcs`` container is confirmed to be up and running on the passive OIM node.