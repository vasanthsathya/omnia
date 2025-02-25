Execute local repo playbook
=============================

The local repository playbook (``local_repo.yml``) downloads and saves the software packages/images to the **Pulp container**, which all the cluster nodes can access.

Configurations made by the playbook
--------------------------------------

    * Creates the Omnia local registry on the OIM at ``<OIM IP>:5001``.

    * If ``repo_config`` in ``input/software_config.json`` is set to ``always``, all images present in the ``input/config/<cluster_os_type>/<cluster_os_version>`` folder will be downloaded to the OIM.

        * If the image is defined using a tag, the image will be tagged using ``<OIM IP>:5001/<image_name>:<version>`` and pushed to the Omnia local registry.

        * If the image is defined using a digest, the image will be tagged using ``<OIM IP>:5001/<image_name>:omnia`` and pushed to the Omnia local registry.


    * When  ``repo_config`` in ``input/software_config.json`` is set to ``always``, the OIM is set as the default registry mirror.

Playbook execution
----------------------

To create local repositories on the Pulp container, execute the ``local_repo.yml`` playbook using the following command: ::

    ssh omnia_core
    cd /omnia/local_repo
    ansible-playbook local_repo.yml

Check status of the packages
------------------------------

After ``local_repo.yml`` has been executed, a status report is displayed containing the status for each downloaded package along with the complete playbook execution time. Here's an example of what that might look like:

.. image:: ../../../images/local_repo_status.png

**SUCCESS**: The package has been successfully downloaded to the Pulp container.

**SKIPPED**: Packages which are already a part of AppStream or BaseOS repositories are not downloaded, and show up as ``SKIPPED`` in the status report.

**FAILED**: The package couldn't be downloaded successfully.

.. note::

    * The ``local_repo.yml`` playbook execution fails if any software package has a ``FAILED`` status. In such a scenario, the user needs to re-run the ``local_repo.yml`` playbook.

    * If any software package fails to download during the execution of this playbook, other scripts/playbooks that rely on the package may also fail.

    * To download additional software packages after the playbook has been executed, simply update the ``input/project_default/software_config.json`` with the new software information and re-run the ``local_repo.yml`` playbook.

    * After ``local_repo.yml`` has run, the value of ``repo_config`` in ``input/project_default/software_config.json`` cannot be updated without running the `oim_cleanup.yml <../../Maintenance/cleanup.html>`_ playbook first.

Log files
----------

The ``local_repo.yml`` playbook generates and provides two types of log files as part of its execution:

1. ``standard.log``: This log file is present in the ``opt/omnia/offline_repo/<node_group>`` directory, and contains the overall status of the ``local_repo.yml`` playbook execution.

2. Package based logs: Each package download initiated by the ``local_repo.yml`` playbook comes with its own log file. These log files can be accessed from ``opt/omnia/offline_repo/<node_group>/<package_name>/logs``.

.. note:: To view the log files in ``.csv`` format, navigate to ``/opt/omnia/offline_repo/<node_group>/status.csv``.

Here's an example of how the log files are organized in the ``opt/omnia/offline_repo/<node_group>`` directory:

.. image:: ../../../images/local_repo_logs.png

**[Optional]** `Update all local repositories <update_local_repo.html>`_