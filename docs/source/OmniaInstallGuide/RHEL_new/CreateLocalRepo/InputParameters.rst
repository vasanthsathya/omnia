Input parameters for Local Repositories
==========================================

The ``local_repo_utility.yml`` playbook is dependent on the inputs provided to the following input files:

* ``input/project_default/software_config.json``
* ``input/project_default/local_repo_config.yml``

``input/project_default/software_config.json``
-----------------------------------------------------

Based on the inputs provided to the ``input/project_default/software_config.json``, the software packages/images are accessed from the Pulp container and the desired software stack is deployed on the cluster nodes.

.. csv-table:: Parameters for Software Configuration
   :file: ../../../Tables/software_config_rhel.csv
   :header-rows: 1
   :keepspace:
   :widths: auto

A sample version for RHEL is provided below:

::

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

.. note::

    * For a list of accepted ``softwares``, go to the ``input/project_default/config/<cluster_os_type>/<cluster_os_version>`` and view the list of JSON files available. The filenames present in this location are the list of accepted softwares. For example, for a cluster running RHEL 9.4, go to ``input/config/rhel/9.4/`` and view the file list for accepted softwares.
    * Omnia supports a single version of any software packages in the ``input/project_default/software_config.json`` file. Ensure that multiple versions of the same package is not mentioned.
    * To configure a locally available repository that does not have a pre-defined json file, `click here <../AdvancedConfigurationsRHEL/CustomLocalRepo.html>`_.

``input/project_default/local_repo_config.yml``
------------------------------------------------------

.. csv-table:: Parameters for Local Repository Configuration
   :file: ../../../Tables/local_repo_config_rhel.csv
   :header-rows: 1
   :keepspace:
   :widths: auto