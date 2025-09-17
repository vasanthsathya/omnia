Sample Files
=============

inventory file
-----------------

.. caution:: All the file contents mentioned below are case sensitive.

::

    [bmc]
    10.3.0.101
    10.3.0.102

.. note::

            * For Slurm, all the applicable inventory groups are ``service_kube_node_x86_64``, ``slurm_control_node_x86_64`` , and ``slurm_node_x86_64``.
            * For Kubernetes, all the applicable groups are ``service_kube_node_x86_64``, ``kube_node``, and ``etcd``.
            * For secure login node functionality, ensure to add the ``login_node_x86_64`` and ``slurm_control_node_x86_64`` groups in the provided inventory file.

software_config.json for RHEL
-------------------------------------------

::

    {
    "cluster_os_type": "rhel",
    "cluster_os_version": "10.0",
    "repo_config": "always",
    "softwares": [
        {"name": "cuda", "version": "12.9.1", "arch": ["x86_64","aarch64"]},
        {"name": "ofed", "version": "24.10-3.2.5.0", "arch": ["x86_64"]},
        {"name": "openldap", "arch": ["x86_64"]},
        {"name": "nfs", "arch": ["x86_64","aarch64"]},
        {"name": "service_k8s","version": "1.31.4", "arch": ["x86_64"]},
        {"name": "slurm", "arch": ["x86_64","aarch64"]}
    ],
    "slurm": [
        {"name": "slurm_control_node"},
        {"name": "slurm_node"},
        {"name": "login_node"}
    ]
 
    }

pxe_mapping_file.csv
------------------------------------

::

    FUNCTIONAL_GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slurm_controller_node_x86_64,x1000c1s7b1n0,n1,xx:yy:zz:aa:bb:cc,10.5.0.101,xx:yy:zz:aa:bb:dd,10.3.0.101
    slurm_node_x86_64,x1000c1s7b1n1,n2,aa:bb:cc:dd:ee:ff,10.5.0.102,aa:bb:cc:dd:ee:gg,10.3.0.102