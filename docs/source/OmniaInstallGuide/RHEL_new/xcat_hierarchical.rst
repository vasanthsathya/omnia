Step 3: Hierarchical Cluster
==================================

In order to manage large-sized clusters, Omnia helps to create a hierarchical cluster based on user inputs. A **hierarchical cluster** organizes nodes in layers, with a central **Management Node (MN)** overseeing multiple **Service Nodes (SN)**, each managing a group of compute nodes. 
To know more, `click here <https://xcat-docs.readthedocs.io/en/stable/advanced/hierarchy/index.html>`_.

A typical hierarchical cluster consists of:

* **Management Node**: The top-level node that oversees the entire cluster.

* **Service Nodes**: Intermediate nodes that manage groups of compute nodes. These handle hardware provisioning, OS-deployment, monitoring, and commands for their assigned nodes.

* **Compute Nodes**: The actual worker nodes of the cluster.

.. image:: ../../images/xcat_hierarchical.png
    :width: 300px

Omnia supports hierarchical cluster formation only when ``service_node`` role is defined in ``roles_config.yml`` input file under the ``/opt/omnia/input/project_default/`` directory, where compute nodes will be associated with their respective service node. 
If ``service_node`` role is not defined then all nodes will be provisioned from the OIM. For more information, `click here <composable_roles.html>`_.

.. note:: To support hierarchical provisioning, all the SNs (active or passive) should be in booted state.


Omnia also supports HA functionality for the ``OIM``, ``service_node``, and ``kube_control_plane`` of the management layer. For more information, `click here <HighAvailability/index.html>`.

.. note:: 
    
    * In a hierarchical cluster setup, an external NFS share must be used for the Omnia shared path.
    * If you want to use HA functionality, ensure that all the nodes (active or passive) are in booted state.