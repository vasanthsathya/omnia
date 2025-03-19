Step 2: Provide all credentials required during Omnia's execution
===================================================================

Omnia provides an additional utility playbook called ``credential_utility.yml``. This playbook upon execution creates an input file called ``omnia_credentials.yml`` in the ``/opt/omnia/input/project_default`` folder.
In this input file, you can provide all types of mandatory and optional credentials required by Omnia during its execution.

Prerequisite
---------------

Ensure that the ``omnia_core`` container is up and running.

Task performed by the playbook
---------------------------------

Creates an input file called ``omnia_credentials.yml`` in the ``/opt/omnia/input/project_default`` folder.

Execute the playbook
----------------------

To execute the playbook, run the following command: ::

    ssh omnia_core
    cd /omnia
    ansible-playbook credential_utility.yml

Post execution
----------------

After the playbook has been executed, navigate to the ``omnia_credentials.yml`` input file is present in the ``/opt/omnia/input/project_default`` folder.
Provide all required credentials for the cluster. See the list below to know more:

.. csv-table:: Credentials required by Omnia
    :file: ../../Tables/omnia_credentials.csv
    :header-rows: 1
    :keepspace: