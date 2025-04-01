Composable roles in omnia
============================

In Omnia, nodes are organized based on their assigned roles. Nodes with the same role can be clubbed under a group. By combining both roles and groups, Omnia offers a powerful and flexible approach to managing large-scale node infrastructures, ensuring both logical organization and physical optimization of resources.

* **Role**: A role defines what a node does in the system. It is a way to categorize nodes based on their functionality. For example, a node could have the role of a Login server, a Compiler, a K8Worker (Kubernetes Worker), or a SLURMWorker (a node in a slurm job scheduler system). Roles help group nodes that perform similar tasks, making it easier to manage and assign resources.

* **Group**: A group is based on the physical characteristics of the nodes. It refers to nodes that are located in the same place or have similar hardware. For example, nodes in the same rack or SU (service unit) might be grouped together, with specific roles like HeadNode or ServiceNode. Groups help with physical organization and management of nodes.

Prerequisites
---------------

* Ensure that the ``roles_config.yml`` input file in the ``input/project_default`` directory includes all necessary attributes for the nodes, based on their role/group within the cluster. Each role/group will have following attributes as indicated in the table below:

    .. csv-table:: Roles and their attributes
       :file: ../../Tables/composable_roles.csv
       :header-rows: 1
       :keepspace:


Roles offered by Omnia
-------------------------

.. note:: 
    
    * Nested roles and groups are not supported.
    * Maximum number of supported roles are 100.
    * Atleast one role is mandatory, and you must not change the name of the roles.
    * The roles are case-sensitive in nature.

.. csv-table:: roles_config.yml
   :file: ../../Tables/omnia_roles.csv
   :header-rows: 1
   :keepspace: