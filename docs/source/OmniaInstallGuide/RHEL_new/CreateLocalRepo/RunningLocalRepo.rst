Execute local repo playbook
=============================

The local repository playbook (``local_repo_utility.yml``) downloads and saves the software packages/images to the **Pulp container**, which all the cluster nodes can access.

Configurations made by the playbook
--------------------------------------

    * Creates the Omnia local registry on the OIM at ``<OIM IP>:5001``.

    * If ``repo_config`` in ``input/software_config.json`` is set to ``always``, all images present in the ``input/config/<cluster_os_type>/<cluster_os_version>`` folder will be downloaded to the OIM.

        * If the image is defined using a tag, the image will be tagged using ``<OIM IP>:5001/<image_name>:<version>`` and pushed to the Omnia local registry.

        * If the image is defined using a digest, the image will be tagged using ``<OIM IP>:5001/<image_name>:omnia`` and pushed to the Omnia local registry.


    * When  ``repo_config`` in ``input/software_config.json`` is set to ``always``, the OIM is set as the default registry mirror.

Playbook execution
----------------------

To create local repositories on the Pulp container, execute the ``local_repo_utility.yml`` playbook using the following command: ::

    ssh omnia_core
    cd /omnia/local_repo
    ansible-playbook local_repo_utility.yml

Verify the creation of the local repositories
-------------------------------------------------

After ``local_repo_utility.yml`` has been executed, a status report is displayed containing the status for each package download and the playbook execution time. The corresponding log file for each package download can be located at ``/opt/omnia/....``. Here's an example of what that might look like:

.. images:: ../../../images/local_repo_status.png

**SUCCESS**: The package have been successfully downloaded to the Pulp container.
**SKIPPED**: Packages which are already a part of AppStream or BaseOS repositories show up as ``SKIPPED``.
**FAILED**: The package download has failed.

.. note::
    * View the status of packages for the current run of ``local_repo_utility.yml`` in ``/opt/omnia/offline/download_package_status.csv``.

    * ``local_repo_utility.yml`` playbook execution fails if any software package has ``FAILED`` status. In such a scenario, the user needs to re-run ``local_repo_utility.yml``.

    * If any software package fails to download during the execution of this playbook, other scripts/playbooks that rely on the package may also fail.

    * After ``local_repo_utility.yml`` has run, the value of ``repo_config`` in ``input/project_default/software_config.json`` cannot be updated without running the `oim_cleanup.yml <../../Maintenance/cleanup.html>`_ playbook first.

    * To download additional software packages after the playbook has been executed, simply update the ``input/project_default/software_config.json`` new software information and re-run ``local_repo_utility.yml``.

**[Optional]** `Update all local repositories <update_local_repo.html>`_