Update all local repositories
===============================

This playbook updates the repository configurations on compute nodes by creating ``.repo`` files whenever new user repositories or Omnia repositories are added in the 
``input/local_repo_config.yml`` or versioned software entry like ``amdgpu``, ``beegfs``, or ``rocm`` is 
included in ``input/software_config.json``.

This playbook should be executed if:

* New user repositories are added in ``input/local_repo_config.yml``
* New Omnia repositories are added in ``input/local_repo_config.yml``
* ``amdgpu``, ``beegfs``, or ``rocm`` is added to ``input/software_config.json``

.. note:: After adding a new repository or software, first run the ``local_repo.yml`` playbook, followed by this playbook to update the configurations on all compute nodes.

Playbook execution
-------------------

To execute the playbook: ::

    ssh omnia_core
    cd /omnia/utils
    ansible-playbook update_user_repo.yml -i <inventory_filepath>
 
*<inventory_filepath> refers to the path of the Kubernetes or Slurm inventory.*