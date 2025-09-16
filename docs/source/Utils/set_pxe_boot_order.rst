Set PXE Boot Order
====================

When PXE boot order is set on a node in Omnia, the node automatically retrieves and boots into the diskless image provided by the Omnia Infrastructure Manager (OIM).

To configure PXE boot for nodes after they are discovered with the ``discovery.yml`` playbook, do the following:

1. Generate the inventory file based on the mapping file.

   **Sample mapping file**::

   FUNCTIONAL_GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
   slurm_controller_node_x86_64,x1000c1s7b1n0,n1,xx:yy:zz:aa:bb:cc,10.5.0.101,xx:yy:zz:aa:bb:dd,10.3.0.101
   slurm_node_x86_64,x1000c1s7b1n1,n2,aa:bb:cc:dd:ee:ff,10.5.0.102,aa:bb:cc:dd:ee:gg,10.3.0.102

   **Sample inventory file**::

      [bmc]
      10.3.0.101
      10.3.0.102

2. Run the following playbook to configure PXE boot on the nodes using the inventory file::

      ansible-playbook set_pxe_boot.yml -i inventory


