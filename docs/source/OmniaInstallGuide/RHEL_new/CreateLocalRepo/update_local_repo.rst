Update all local repositories
===============================

This playbook updates all local repositories configured on a provisioned cluster after local repositories have been configured. Use the following command to run the playbook: ::

    ssh omnia_core
    cd /omnia/utils
    ansible-playbook update_user_repo.yml -i <inventory filepath>