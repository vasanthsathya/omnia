Space requirements for the OIM running on RHEL or Rocky Linux OS
=====================================================================

* Entire software stack that Omnia supports: 50GB
* To keep all the software images in ``/`` or ``/var`` partition: 500GB
.. note:: For nodes with limited storage space in ``/`` or ``/var`` partition, Omnia suggests to execute ``local_repo.yml`` playbook with ``repo_config`` set to ``never`` in ``input/local_repo_config.yml``. In this scenario, all software packages are downloaded and stored in pre-defined user registry.
* To store offline repositories (the file path should be specified in ``repo_store_path`` in ``input/local_repo_config.yml``): 50GB

.. note:: Docker and nerdctl services operate from the ``/var/lib/<docker or nerdctl>`` directory. If the OIM has storage constraints, users can mount this directory to another drive of their choice that has more storage capacity. Also, the user can mount any external NFS server on the OIM and use that to store the software packages.

.. csv-table:: Space requirements for images and packages on OIM
   :file: ../../Tables/RHEL_space_req.csv
   :header-rows: 1
   :keepspace:

.. [1] Space allocated as part of OS repository (.iso). No extra space required.
