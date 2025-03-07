Step 2: Provide all credentials required during Omnia's execution
===================================================================

Omnia provides an additional utility playbook called ``credential_utility.yml``. This playbook upon execution creates an input file called ``omnia_credentials.yml`` in the ``/opt/omnia/input/project_default`` folder.
In this input file, you can provide all types of mandatory and optional credentials required by Omnia during its execution.

Prerequisites
---------------


Tasks performed by the playbook
---------------------------------


Execute the playbook
----------------------

To execute the playbook, run the following command: ::

    ssh omnia_core
    cd /omnia
    ansible-playbook credential_utility.yml