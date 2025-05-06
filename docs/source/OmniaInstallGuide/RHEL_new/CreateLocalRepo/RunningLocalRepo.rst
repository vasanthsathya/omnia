Execute local repo playbook
=============================

The local repository playbook (``local_repo.yml``) downloads and saves the software packages/images to the **Pulp container**, which all the cluster nodes can access.

Configurations made by the playbook
--------------------------------------

    * With ``repo_config`` set to ``always`` in ``/opt/omnia/input/project_default/config/software_config.json``, all images and artifacts will be downloaded to the Pulp container present on the NFS share.

    * If  ``repo_config`` in is set to ``always``, the OIM serves as the default Pulp registry.

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

**FAILED**: The package couldn't be downloaded successfully.

.. note::

    * The ``local_repo.yml`` playbook execution fails if any software package has a ``FAILED`` status. In such a scenario, the user needs to re-run the ``local_repo.yml`` playbook.

    * If any software package fails to download during the execution of this playbook, other scripts/playbooks that rely on the package may also fail.

    * To download additional software packages after the playbook has been executed, simply update the ``/opt/omnia/input/project_default/software_config.json`` with the new software information and re-run the ``local_repo.yml`` playbook.

Log files
----------

The ``local_repo.yml`` playbook generates and provides two types of log files as part of its execution:

1. ``standard.log``: This log file is present in the ``/opt/omnia/log/local_repo`` directory, and contains the overall status of the ``local_repo.yml`` playbook execution.

2. **Package based logs**: Each package download initiated by the ``local_repo.yml`` playbook comes with its own log file. These log files can be accessed from ``/opt/omnia/log/local_repo``.

.. note:: To view the log files in ``.csv`` format, navigate to ``/opt/omnia/log/local_repo/status.csv``.

Here's an example of how the log files are organized in the ``/opt/omnia/log/local_repo`` directory:

.. image:: ../../../images/local_repo_log.png

**[Optional]** `Update all local repositories <update_local_repo.html>`_