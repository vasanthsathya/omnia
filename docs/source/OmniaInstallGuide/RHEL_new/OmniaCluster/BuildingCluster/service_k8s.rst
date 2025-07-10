=================================
Service Kubernetes (K8s) cluster
=================================

Omnia supports deploying Kubernetes on the service cluster via the ``service_k8s_cluster.yml`` playbook.

Prerequisite
==============

To deploy Kubernetes on service cluster, ``k8s`` and ``service_k8s`` must be added under ``softwares`` in the ``input/software_config.json``. Refer the sample config file below: ::

    {
        "cluster_os_type": "rhel",
        "cluster_os_version": "9.6",
        "iso_file_path": "",
        "repo_config": "always",
        "softwares": [
            {"name": "amdgpu", "version": "6.3.1"},
            {"name": "cuda", "version": "12.8.0"},
            {"name": "ofed", "version": "24.10-1.1.4.0"},
            {"name": "service_node" },
            {"name": "openldap"},
            {"name": "nfs"},
            {"name": "k8s", "version":"1.31.4"},
            {"name": "service_k8s","version": "1.31.4"},
            {"name": "slurm"}
        ],
        "amdgpu": [
            {"name": "rocm", "version": "6.3.1" }
        ],
        "slurm": [
            {"name": "slurm_control_node"},
            {"name": "slurm_node"},
            {"name": "login"}
        ]
    }

Steps
=======

1. Run ``prepare_oim.yml`` playbook to bring up the required containers on the service cluster nodes.

2. Run ``local_repo.yml`` playbook to download the artifacts required to set up Kubernetes on the service cluster nodes.

3. Run ``discovery_provision.yml`` playbook to discover and provision OS on the service cluster nodes.

4. Fill in the required paramters in ``roles_config.yml``, ``omnia_config.yml``, and ``high_availability_config.yml`` as described in the tables below:



Playbook execution
====================

Once all the required input files are filled up, use the below commands to set up Kubernetes on the service cluster: ::

    cd scheduler
    ansible-playbook service_k8s_cluster.yml - i <service_cluster_inventory_filepath>