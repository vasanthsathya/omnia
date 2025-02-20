Step 4: Create Local repositories for the cluster
==================================================

The ``local_repo_utility.yml`` playbook facilitates Airgap installation (without access to public network) on the cluster nodes, and is invoked from inside the ``omnia_core`` container. It deploys the **Pulp container** on an NFS share, which acts as a centralized storage unit and hosts all software packages and images required and supported by Omnia. These packages or images are then accessed by the cluster nodes from that NFS share.

Once the container is ready, you can provide inputs in the ``/input/project_default/software_config.json`` and ``/input/project_default/local_repo_config.yml``, based on which the desired packages or images will be accessed from the container and downloaded onto the cluster nodes (without accessing the internet).

.. toctree::
    Prerequisite
    InputParameters
    localrepos
    RunningLocalRepo

