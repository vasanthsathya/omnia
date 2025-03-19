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

Things to keep in mind
------------------------

* While executing any Omnia playbook which requires certain credentials, you'll now see a prompt to enter them during playbook execution.
* Credential fields which have the tag ``mandatory`` cannot be left empty. If the ``mandatory`` passwords are not provided or incorrect, the playbook execution will stop and exit while encrypting the credentials file in the background.
* Credential fields which have the tag ``Optional`` can be skipped. Even if not input is provided, playbook execution will continue.
* Credential fields which have the tag ``default`` can also be skipped or left empty. In this case, Omnia appends a default value to that field and proceeds with the playbook execution.
* Passwords provided by you will be hidden. You must enter the password for a second time to confirm.
* This utility also supports using tags to provide credentials for specific features or packages. For example, you can use ``--tags provision`` while executing the playbook to only bring up the credentials required to provision the cluster nodes.

Post execution
----------------

After the playbook has been executed, navigate to the ``omnia_credentials.yml`` input file is present in the ``/opt/omnia/input/project_default`` folder.
Provide all required credentials for the cluster. See the list below to know more:

.. csv-table:: Credentials required by Omnia
    :file: ../../Tables/omnia_credentials.csv
    :header-rows: 1
    :keepspace:

