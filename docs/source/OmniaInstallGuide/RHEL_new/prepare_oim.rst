Step 3: Execute the ``prepare_oim.yml`` playbook
==================================================

The ``prepare_oim.yml`` playbook is the first playbook that you need to run in Omnia. This playbook accomplishes the following tasks:

* Sets up the PCS container: ``omnia_pcs``
* Sets up the Kubespray container: ``omnia_kubespray_<version>``
* Sets up the Provision container: ``omnia_provision``

Input files for the playbook
------------------------------

The ``prepare_oim.yml`` playbook is dependent on the inputs provided to the following input files:

* ``network_spec.yml``: This input file is located in the ``/opt/omnia/input`` folder and contains the necessary configurations for the cluster network.
* ``provision_config_credentials.yml``: This input file is located in the ``/opt/omnia/input`` folder and contains the necessary passwords required for provisioning the cluster.
* ``software_config.json``: This input file is located in the ``/opt/omnia/input`` folder and contains the details about the software packages which are to be installed on the cluster.

1. ``network_spec.yml``
------------------------

Add necessary inputs to the ``network_spec.yml`` file to configure the network on which the cluster will operate. Use the below table as reference while doing so:

.. csv-table:: network_spec.yml
   :file: ../../Tables/network_spec.csv
   :header-rows: 1
   :keepspace:

.. note::

    * If the ``nic_name`` is identical on both the ``admin_network`` and the ``bmc_network``, it indicates a LOM setup. Otherwise, it's a dedicated setup.
    * BMC network details are not required when target nodes are discovered using a mapping file.
    * If ``bmc_network`` properties are provided, target nodes will be discovered using the BMC method in addition to the methods whose details are explicitly provided in ``provision_config.yml``.
    * The strings ``admin_network`` and ``bmc_network`` in the ``input/network_spec.yml`` file should not be edited. Also, the properties ``nic_name``, ``static_range``, and ``dynamic_range`` cannot be edited on subsequent runs of the provision tool.
    * ``netmask_bits`` are mandatory and should be same for both ``admin_network`` and ``bmc_network`` (that is, between 1 and 32; 1 and 32 are also acceptable values).

.. caution::
    * Do not assign the subnet 10.4.0.0/24 to any interfaces in the network as nerdctl uses it by default.
    * All provided network ranges and NIC IP addresses should be distinct with no overlap in the ``input/network_spec.yml``.
    * Ensure that all the iDRACs are reachable from the OIM.

A sample of the ``input/network_spec.yml`` where nodes are discovered using a **mapping file** is provided below: ::

    ---
         Networks:
         - admin_network:
             nic_name: "eno1"
             netmask_bits: "16"
             static_range: "10.5.0.1-10.5.0.200"
             dynamic_range: "10.5.1.1-10.5.1.200"
             correlation_to_admin: true
             admin_uncorrelated_node_start_ip: "10.5.0.50"
             primary_oim_admin_ip: "10.5.255.254"
             network_gateway: ""
             DNS: ""
             MTU: "1500"

         - bmc_network:
             nic_name: ""
             netmask_bits: ""
             static_range: ""
             dynamic_range: ""
             reassignment_to_static: true
             discover_ranges: ""
             network_gateway: ""
             MTU: "1500"

A sample of the ``input/network_spec.yml`` where nodes are discovered using **BMC discovery mechanism** is provided below: ::

    ---
        Networks:
        - admin_network:
            nic_name: ""
            netmask_bits: ""
            static_range: ""
            dynamic_range: ""
            correlation_to_admin: true
            admin_uncorrelated_node_start_ip: ""
            primary_oim_admin_ip: ""
            network_gateway: ""
            DNS: ""
            MTU: ""

        - bmc_network:
            nic_name: "eno1"
            netmask_bits: "16"
            static_range: "10.3.0.1-10.3.0.200"
            dynamic_range: "10.3.1.1-10.3.1.200"
            reassignment_to_static: true
            discover_ranges: ""
            network_gateway: ""
            MTU: "1500"

2. ``provision_config_credentials.yml``
-----------------------------------------

Add necessary inputs to the ``provision_config_credentials.yml`` file for seamless authentication during cluster provisioning. Use the below table as reference while doing so:

.. csv-table:: provision_config_credentials.yml
   :file: ../../Tables/Provision_creds.csv
   :header-rows: 1
   :keepspace:

3. ``software_config.json``
-------------------------------

The ``software_config.json`` file lists all the software packages to be installed on the OIM. Edit the ``software_config.json`` file based on the software stack you want on the OIM. Use the below table as reference while doing so:

.. csv-table:: software_config.json
   :file: ../../Tables/software_config_rhel.csv
   :header-rows: 1
   :keepspace:

A sample of the ``software_config.json`` file for RHEL clusters is attached below: ::

    {
        "cluster_os_type": "rhel",
        "cluster_os_version": "9.4",
        "repo_config": "always",
        "softwares": [
            {"name": "amdgpu", "version": "6.2.2"},
            {"name": "cuda", "version": "12.3.2"},
            {"name": "ofed", "version": "24.01-0.3.3.1"},
            {"name": "freeipa"},
            {"name": "openldap"},
            {"name": "secure_login_node"},
            {"name": "nfs"},
            {"name": "beegfs", "version": "7.4.2"},
            {"name": "slurm"},
            {"name": "k8s", "version":"1.29.5"},
            {"name": "jupyter"},
            {"name": "kubeflow"},
            {"name": "kserve"},
            {"name": "pytorch"},
            {"name": "tensorflow"},
            {"name": "vllm"},
            {"name": "telemetry"},
            {"name": "intel_benchmarks", "version": "2024.1.0"},
            {"name": "amd_benchmarks"},
            {"name": "utils"},
            {"name": "ucx", "version": "1.15.0"},
            {"name": "openmpi", "version": "4.1.6"},
            {"name": "csi_driver_powerscale", "version":"v2.11.0"}
        ],

        "amdgpu": [
            {"name": "rocm", "version": "6.2.2" }
        ],
        "vllm": [
            {"name": "vllm_amd"},
            {"name": "vllm_nvidia"}
        ],
        "pytorch": [
            {"name": "pytorch_cpu"},
            {"name": "pytorch_amd"},
            {"name": "pytorch_nvidia"}
        ],
        "tensorflow": [
            {"name": "tensorflow_cpu"},
            {"name": "tensorflow_amd"},
            {"name": "tensorflow_nvidia"}
        ]
    }

Playbook execution
-------------------

After you have filled in the input files as mentioned above, execute the following commands to trigger the playbook: ::

    ssh omnia_core
    cd /omnia/prepare_oim
    ansible-playbook prepare_oim.yml