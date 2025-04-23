Step 3: Hierarchical Cluster
==================================

Omnia v2.0 supports Hierarchical cluster provisioning.

Hierarchical cluster
----------------------

In order to manage large-sized clusters, Omnia helps to create a hierarchical cluster. A **hierarchical cluster** organizes nodes in layers, with a central **Management Node (MN)** overseeing multiple **Service Nodes (SN)**, each managing a group of compute nodes. To know more, `click here <https://xcat-docs.readthedocs.io/en/stable/advanced/hierarchy/index.html>`_.

A typical hierarchical cluster consists of:

* **Management Node**: The top-level node that oversees the entire cluster.

* **Service Nodes**: Intermediate nodes that manage groups of compute nodes. These handle hardware provisioning, OS-deployment, monitoring, and commands for their assigned nodes.

* **Compute Nodes**: The actual worker nodes of the cluster.

.. image:: ../../images/xcat_hierarchical.png
    :width: 300px

Hierarchical cluster in Omnia
-------------------------------

Omnia supports hierarchical cluster formation only when ``service_node`` role is defined in ``roles_config.yml`` input file under the ``/opt/omnia/input/project_default/`` directory, where compute nodes will be associated with their respective service node. 
If ``service_node`` role is not defined then all nodes will be provisioned from the OIM. For more information, `click here <composable_roles.html>`_.