Step 2: Composable groups and functional groups in Omnia
============================================================

In Omnia, nodes are organized based on their assigned groups and functional groups. By combining both groups and functional groups, Omnia offers a powerful and flexible approach to managing large-scale node infrastructures, ensuring both logical organization and physical optimization of resources.

* **Functional Group**: A functional group defines what a node does in the system. It is a way to categorize nodes based on their functionality. For example, a node could have the functional group of a Login server, a Compiler, a K8Worker (Kubernetes Worker), or a SLURMWorker (a node in a slurm job scheduler system). Functional groups help group nodes that perform similar tasks, making it easier to manage and assign resources.

* **Group**: A group is based on the physical characteristics of the nodes. It refers to nodes that are located in the same place or have similar hardware. For example, nodes in the same rack or SU (Scalable Unit) might be grouped together, with specific functional groups like HeadNode or ServiceNode. Groups help with physical organization and management of nodes.

Functional groups offered by Omnia
-------------------------------------

.. note:: 
    
    * Nested functional groups and groups are not supported.
    * Maximum number of supported functional groups are 100.
    * At least one functional group is mandatory, and you must not change the name of functional groups.
    * The functional groups are case-sensitive in nature.
    * Groups assigned to the **Management** layer functional groups should not be assigned to **Compute** layer functional groups.
    * Omnia also supports HA functionality for the ``OIM`` and the ``service_cluster``. For more information, `click here <HighAvailability/index.html>`_.
    * To set up a service cluster, all three functional groups (``service_kube_control_plane``, ``service_etcd``, ``service_kube_node``) must be present in the ``input/roles_config.yml``.

.. csv-table:: Types of Functional Groups
   :file: ../../Tables/omnia_roles.csv
   :header-rows: 1
   :keepspace:

Group attributes
----------------

Nodes with similar roles or functionalities can be grouped together. To do so, fill up the ``roles_config.yml`` input file in the ``/opt/omnia/input/project_default`` directory which includes all necessary attributes for the nodes, based on their role within the cluster. Each group will have following attributes as indicated in the table below:

.. csv-table:: Group attributes
   :file: ../../Tables/group_attributes.csv
   :header-rows: 1
   :keepspace:
   
Sample
-------

Here's a sample (using mapping file) for your reference:

::
    
    groups:
        grp0:
            location_id: SU-1.RACK-1
            cluster_name: ""
            parent: ""
            architecture: "x86_64"

        grp1:
            location_id: SU-1.RACK-2
            cluster_name: "slurm_node_cluster"
            parent: ""
            architecture: "aarch64"

    functional_groups:
        - name: "default"
          groups:
            - grp0

        - name: "slurm_node"
          groups:
            - grp1


