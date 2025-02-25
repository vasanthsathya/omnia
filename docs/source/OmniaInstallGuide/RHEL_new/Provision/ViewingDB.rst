Checking node status
----------------------

Via CLI
--------

* Establish a SSH connection to the ``omnia_core`` container using the following command: ::

    ssh omnia_core

* After you're in the ``omnia_core`` container, use SSH again to reach the ``omnia_provision`` container: ::

    ssh omnia_provision

* Run ``nodels all nodelist.status`` for a list of nodes and their statuses. Here's an example of this command output: ::

    omnia-node00001: installing
    omnia-node00002: booted
    omnia-node00003: powering-on
    omnia-node00004: booted

Possible values of node status are ``powering-off``, ``powering-on``, ``bmcready``, ``installing``, ``booting``, ``post-booting``, ``booted``, and ``failed``.

Via Omnia database [omniadb]
-----------------------------

* To access the omniadb, execute: ::

            psql -U postgres

            \c omniadb


* To view the schema being used in the cluster: ``\dn``

* To view the tables in the database: ``\dt``

* To view the contents of the ``nodeinfo`` table: ``select * from cluster.nodeinfo;`` ::

         id | service_tag |     node      |   hostname     |     admin_mac     |   admin_ip   |   bmc_ip   | status | discovery_mechanism | bmc_mode | switch_ip | switch_name | switch_port | cpu | gpu | cpu_count | gpu_count$
        ----+-------------+---------------+----------------+-------------------+--------------+------------+--------+---------------------+----------+-----------+-------------+-------------+-----+-----+-----------+------------
          1 |             | oim           | newoim.new.dev | 00:0a:f7:dc:11:42 | 10.5.255.254 | 0.0.0.0    |        |                     |          |           |             |             |     |     |           |
          2 | xxxxxxx     | node2         | node2.new.dev  | c4:cb:e1:b5:70:44 | 10.5.0.12    | 10.30.0.12 | booted | mapping             |          |           |             |             | amd |     |         1 |         0
          3 | xxxxxxx     | node3         | node3.new.dev  | f4:02:70:b8:bc:2a | 10.5.0.10    | 10.30.0.10 | booted | mapping             |          |           |             |             | amd | amd |         2 |         1

Possible values of node status are ``powering-off``, ``powering-on``, ``bmcready``, ``installing``, ``booting``, ``post-booting``, ``booted``, ``failed``, ``ping``, ``noping``, and ``standingby``.

.. note::
    * The ``gpu_count`` in the database is only updated every time a cluster node is PXE booted.
    * Nodes listed as "failed" can be diagnosed using the ``/var/log/xcat/xcat.log`` file on the target node. Correct any underlying issues and `re-provision the cluster <../../Maintenance/reprovision.html>`_.
    * Information on debugging nodes stuck at ``powering-on``, ``bmcready``, or ``installing`` for longer than expected is available `here <../../../Troubleshooting/FAQ/Common/Provision.html>`_. Correct any underlying issue on the node and `re-provision the cluster <../../Maintenance/reprovision.html>`_.
    * A blank node status indicates that no attempt to provision it has taken place. Attempt a manual PXE boot on the node to initiate provisioning.
