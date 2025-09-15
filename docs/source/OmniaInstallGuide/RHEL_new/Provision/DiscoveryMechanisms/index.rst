Discovery Mechanisms
=====================

Depending on the values provided in ``/opt/omnia/input/project_default/provision_config.yml``, target nodes can be discovered only using the mapping file.

.. toctree::
    :hidden:

    mappingfile   

``mapping file``
-----------------

Manually collect PXE NIC information for target servers and manually define them to Omnia using the **pxe_mapping_file.csv** file. A sample format is shown below:

::

    FUNCTIONAL_GROUP_NAME,SERVICE_TAG,HOSTNAME,ADMIN_MAC,ADMIN_IP,BMC_MAC,BMC_IP
    slum_node_x86_64,x1000c1s7b1n0,n1,xx:yy:zz:aa:bb:cc,10.5.0.101,10.3.0.101
    login_node_x86_64,x1000c1s7b1n1,n2,aa:bb:cc:dd:ee:ff,10.5.0.102,10.3.0.102

 +---------------------------------------------------------+------------------------------------------------------+
| Pros                                                    | Cons                                                 |
+=========================================================+======================================================+
| Easily customizable if the user maintains a list of     | The user needs to be aware of the MAC/IP mapping     |
| MAC addresses.                                          | required in the network.                             |
+---------------------------------------------------------+------------------------------------------------------+
|                                                         | Servers require a manual PXE boot if iDRAC IPs are   |
|                                                         | not configured.                                      |
+---------------------------------------------------------+------------------------------------------------------+

For more information regarding mapping files, `click here <mappingfile.html>`_




