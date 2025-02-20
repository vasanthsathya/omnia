Step 2: Project-based inputs
==============================

Omnia is now deployed from a project-based approach. This allows multiple users to have different set of configuration files for the same cluster. This is achieved using the ``default.yml`` input file present in the ``/opt/omnia/input`` directory.
By default, the ``project_name`` variable value in ``default.yml`` will be ``project_default``. Users can create their own directory under ``opt/omnia/input`` and update the same under ``project_name``. Each directory will have its own set of configuration files.
After you have executed the ``ssh omnia_core`` command, you can access the ``default.yml`` file which has the following parameter:

    +----------------------------+---------------------------------------------------------------+
    |  Variable Name             |  Description                                                  |
    +============================+===============================================================+
    |  ``project_name``          |  This variable captures the project name for Omnia execution. |
    |                            |  Default value: ``project_default``                           |
    +----------------------------+---------------------------------------------------------------+

Here's an example of what the default ``project_default`` directory contains:

.. image:: ../../images/project_default.png