High Availability (HA) for the Kubernetes cluster
======================================================

Omnia deploys a highly available Kubernetes cluster using the Kubespray container image from the Dell registry. This container contains the Kubespray Ansible playbooks, which are used to deploy Kubernetes (k8s) clusters. Kubespray is an open-source tool designed for simplicity and flexibility, ensuring efficient and correct setup of Kubernetes clusters.

Omnia achieves Kubernetes High Availability (HA) by configuring an internal load balancer called `kube-vip <https://kube-vip.io/>`_. Kube-vip is a tool that enables the use of a Virtual IP (VIP) in Kubernetes clusters to support high availability (HA), particularly for services and load balancer setups. In `AddressResolutionProtocol (ARP) <https://wiki.wireshark.org/AddressResolutionProtocol>`_ mode, kube-vip allows Kubernetes cluster nodes to manage traffic routing directly, removing the need for external load balancers and ensuring seamless service availability.

.. note:: A minimum of 3 provisioned nodes are required to set up Kubernetes HA.

Prerequisites
--------------

* The OIM must have internet connectivity in order to download packages required for cluster deployment and configuration.
* The OIM must have 2 NICs in active state, one for public network and the other for cluster network.
* Ensure that ``prepare_oim.yml`` playbook has executed successfully and all the containers are up and running.
* Ensure that all Kubernetes related packages are available in the Pulp local repository.

.. note:: Before running ``prepare_oim.yml``, disable HTTPS by setting the ``pulp_protocol_https`` to ``false`` in the ``/omnia/prepare_oim/roles/deploy_containers/pulp/tasks/deployment_prereq.yml`` and ``/omnia/local_repo/roles/pulp_validation/vars/main.yml`` files.

Preparing the Kubespray container image
-----------------------------------------

Follow the steps below to prepare the Kubespray container image required by Omnia:

1. Build the Kubespray container from the ``kubespraycontainerfile`` using the following command: ::

    podman build -f kubesprayContainerfile -t omnia-kubespray:latest

2. Upload the Kubespray container image to the Dell registry.

Input Parameters
----------------

* Set the ``enable_k8s_ha`` parameter to ``true`` in the ``/opt/omnia/input/project_default/high_availability_config.yml`` file.
* Fill up the ``virtual_ip_address`` parameter in the ``omnia_config.yml`` config file present in the ``/opt/omnia/input/project_default/`` directory.

    .. csv-table:: Parameters for Kubernetes HA
        :file: ../../../Tables/k8s_ha.csv
        :header-rows: 1
        :keepspace:

Sample inventory for HA
---------------------------

::

    [kube_control_plane]
    10.25.0.2
    10.25.0.4
    10.25.0.6

    [etcd]
    10.25.0.3
    10.25.0.5
    10.25.0.7

    [kube_node]
    10.25.0.1
    10.25.0.3
    10.25.0.5

    [k8s_cluster:children]
    kube_control_plane
    kube_node

    [host]
    10.25.255.254

Playbook execution
--------------------

Once all the details are provided to the input files and the Kubespray container image is uploaded to the Dell registry, the ``omnia.yml`` playbook can be executed to deploy the Kubernetes cluster. ::

    ansible-playbook omnia.yml -i <inventory filepath>

