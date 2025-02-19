Input parameters for Local Repositories
==========================================

The ``local_repo.yml`` playbook is dependent on the inputs provided in the following input files:

* ``input/software_config.json``
* ``local_repo_config.yml``
* ``input/provision_config_credentials.yml``

1. ``input/software_config.json``
------------------------------------

.. csv-table:: Parameters for Software Configuration
   :file: ../../../Tables/software_config_rhel.csv
   :header-rows: 1
   :keepspace:
   :class: longtable

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


For a list of accepted values in ``softwares``, go to ``input/config/<cluster_os_type>/<cluster_os_version>`` and view the list of JSON files available. The filenames present in this location (without the * .json extension) are a list of accepted software names. The repositories to be downloaded for each software are listed the corresponding JSON file. For example, for a cluster running RHEL 9.4, go to ``input/config/rhel/9.4/`` and view the file list:
::

    amdgpu.json
    bcm_roce.json
    beegfs.json
    cuda.json
    jupyter.json
    k8s.json
    kserve.json
    kubeflow.json
    nfs.json
    ofed.json
    openldap.json
    pytorch.json
    tensorflow.json
    vllm.json

For a list of repositories (and their types) configured for AMD GPUs, view the ``amdgpu.json`` file: ::

    {
      "amdgpu": {
        "cluster": [
            {"package": "linux-headers-$(uname -r)", "type": "deb", "repo_name": "jammy"},
            {"package": "linux-modules-extra-$(uname -r)", "type": "deb", "repo_name": "jammy"},
            {"package": "amdgpu-dkms", "type": "deb", "repo_name": "amdgpu"}
        ]
      },
      "rocm": {
        "cluster": [
          {"package": "rocm-hip-sdk{{ rocm_version }}*", "type": "deb", "repo_name": "rocm"}
        ]
      }
    }

.. note:: To configure a locally available repository that does not have a pre-defined json file, `click here <../AdvancedConfigurationsRHEL/CustomLocalRepo.html>`_.

2. ``input/local_repo_config.yml``
-------------------------------------

.. csv-table:: Parameters for Local Repository Configuration
   :file: ../../../Tables/local_repo_config_rhel.csv
   :header-rows: 1
   :widths: auto

3. ``input/provision_config_credentials.yml``
--------------------------------------------------

Provide the ``docker_username`` and ``docker_password`` in the ``input/provision_config_credentials.yml`` file to avoid docker pull-limit issues.