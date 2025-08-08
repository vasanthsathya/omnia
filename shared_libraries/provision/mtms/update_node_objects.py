# Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""This module contains functions for updating node objects."""
import subprocess
import sys

db_path = sys.argv[3]
oim_admin_ip = sys.argv[4]
sys.path.insert(0, db_path)
import omniadb_connection

node_obj_nm = []
GROUPS_STATIC = "all,bmc_static"
GROUPS_DYNAMIC = "all,bmc_dynamic"
CHAIN_SETUP = "runcmd=bmcsetup"
provision_os_image = sys.argv[1]
service_os_image = sys.argv[2]
CHAIN_OS = f"osimage={provision_os_image}"
DISCOVERY_MECHANISM = "mtms"


def get_node_obj():
    """
	Get a list of node objects present in Omnia Infrastrcuture Management (OIM) node

	Returns:
		A list of node object names
	"""

    command = "/opt/xcat/bin/lsdef"
    node_objs = subprocess.run(command.split(), capture_output=True,check=False)
    temp = str(node_objs.stdout).split('\n')
    for i in range(0, len(temp) - 1):
        node_obj_nm.append(temp[i].split(' ')[0])

    update_node_obj_nm()


def update_node_obj_nm(chain_os=CHAIN_OS):
    """
    Updates the node objects in the database.

    - This function establishes a connection with omniadb and retrieves the service tags of the 
      nodes from the cluster.nodeinfo table.
    - It then iterates over the service tags and converts them to lowercase.
    - After that, it iterates over the service tags again and converts them to uppercase.
    - For each service tag, it retrieves the node, admin_ip, bmc_ip, bmc_mode, role, cluster_name, group_name, and
      architecture from the cluster.nodeinfo table.
    - If the bmc_mode is None, it prints "No device is found!".
    - If the bmc_mode is "static", it checks if the service_os_image is not "None" and if the
      role contains the string "service".
    - If both conditions are true, it sets the chain_os variable to "osimage={service_os_image}".
    - It then executes a command to update the node objects using the /opt/xcat/bin/chdef command.
    - If the bmc_mode is "dynamic", it executes a command to update the node objects using the
      /opt/xcat/bin/chdef command.
    - Finally, it closes the cursor and the database connection.

    Parameters:
        chain_os (str): osimage name string

    Returns:
        None
    """

    # Establish a connection with omniadb
    conn = omniadb_connection.create_connection()
    cursor = conn.cursor()
    sql = """
        SELECT service_tag
        FROM cluster.nodeinfo
        WHERE DISCOVERY_MECHANISM = %s
        AND (status IS NULL OR status != 'booted')
        """
    cursor.execute(sql, (DISCOVERY_MECHANISM,))
    serial_output = cursor.fetchall()
    for i, _ in enumerate(serial_output):
        if serial_output[i][0] is not None:
            serial_output[i] = str(serial_output[i][0]).lower()
    for i, _ in enumerate(serial_output):
        print(serial_output[i])
        if serial_output[i][0] is not None:
            serial_output[i] = serial_output[i].upper()
            params = (serial_output[i],)
            sql = """SELECT node, admin_ip, bmc_ip, bmc_mode, role, cluster_name, group_name, architecture
                     FROM cluster.nodeinfo
                     WHERE service_tag = %s"""
            cursor.execute(sql, params)
            node_name, admin_ip, bmc_ip, mode, role, cluster_name, group_name, _ = cursor.fetchone()

            if mode is None:
                print("No device is found!")
            if mode == "static":
                if 'service_node' in role:
                    chain_os = f"osimage={service_os_image}"
                else:
                    chain_os = f"osimage={provision_os_image}"
                command = ["/opt/xcat/bin/chdef", node_name, f"ip={admin_ip}",
                           f"groups={GROUPS_STATIC},{role},{cluster_name},{group_name}",
                           f"chain={chain_os}", f"xcatmaster={oim_admin_ip}"]
                subprocess.run(command, check=False)
            if mode == "dynamic":
                command = ["/opt/xcat/bin/chdef", node_name,
                           f"ip={admin_ip}", f"groups={GROUPS_DYNAMIC}",
                           f"chain={CHAIN_SETUP},{chain_os}",
                           f"bmc={bmc_ip}", f"xcatmaster={oim_admin_ip}"]
                subprocess.run(command,check=False)

    cursor.close()
    conn.close()


get_node_obj()
