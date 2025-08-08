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
#  limitations under the License
#pylint: disable=import-error,no-name-in-module
"""This module contains functions for updating db based on mtms."""
import ipaddress
import sys
import os
import re
import warnings
import correlation_admin_bmc
import modify_network_details

db_path = sys.argv[10]
sys.path.insert(0, db_path)

import omniadb_connection

bmc_static_range = sys.argv[1]
static_stanza_path = os.path.abspath(sys.argv[2])
group_name = sys.argv[3]
domain_name = sys.argv[4]
admin_static_range = sys.argv[5]
admin_subnet = sys.argv[6]
netmask_bits = sys.argv[7]
correlation_status = sys.argv[8]
uncorrelated_admin_start_ip = ipaddress.IPv4Address(sys.argv[9])
location_id = sys.argv[11]
architecture = sys.argv[12]
role = sys.argv[13]
PARENT = sys.argv[14] 
cluster_name = sys.argv[15]
DISCOVERY_MECHANISM = "mtms"
BMC_MODE = "static"
admin_static_start_range = ipaddress.IPv4Address(admin_static_range.split('-')[0])
admin_static_end_range = ipaddress.IPv4Address(admin_static_range.split('-')[1])

def get_next_node_name(cursor):
    """Fetch the next available node name based on the last valid node pattern."""
    query = """
        SELECT node
        FROM cluster.nodeinfo
        WHERE group_name = %s
        ORDER BY node DESC;
    """
    result = cursor.execute(query, (group_name,))
    result = cursor.fetchall()
    # Regular expression pattern: e.g., "grp0node001"
    pattern = re.compile(rf"^{re.escape(group_name)}node(\d{{3}})$")
    for row in result:
        node_name = row[0]
        match = pattern.match(node_name)
        if match:
            last_number = int(match.group(1))
            next_node_name = f"{group_name}node{last_number + 1:03d}"
            return next_node_name

    # No matching node found; return the first node name
    return f"{group_name}node001"

def update_db():
    """
	Updates the database with node information.

	This function establishes a connection with the database and performs the following tasks:
	- Checks if the bmc_static_range is not empty.
	- If it is not empty, it extracts the serial and bmc information from the static_stanza_path.
	- It iterates over the serial and checks if the service tag exists in the cluster.nodeinfo table.
	- If the service tag does not exist, it generates a new node name and host name.
	- It updates the stanza file with the new serial and node.
	- It checks if the bmc_ip is already present in the cluster.nodeinfo table.
	- If the bmc_ip is not present, it calculates the admin_ip based on the bmc_ip and admin_subnet.
	- It checks if the admin_ip is within the admin_static_range.
	- If it is, it checks if the admin_ip is already present in the cluster.nodeinfo table.
	- If it is not present, it inserts the node information into the cluster.nodeinfo table.
	- If the admin_ip is not within the admin_static_range, it calculates the uncorrelated_admin_ip.
	- It inserts the node information into the cluster.nodeinfo table.
	- If the service tag already exists in the cluster.nodeinfo table, it prints a warning.

	Parameters:
	None

	Returns:
	None
	"""

    conn = omniadb_connection.create_connection()
    cursor = conn.cursor()

    if bmc_static_range != "":
        temp = modify_network_details.extract_serial_bmc(static_stanza_path)
        bmc = temp[0]
        serial = temp[1]
        for key, _ in enumerate(serial):
            sql = f"""select exists(select service_tag from cluster.nodeinfo
              where service_tag='{serial[key]}')"""
            cursor.execute(sql)
            output = cursor.fetchone()[0]
            bmc_output = modify_network_details.check_presence_bmc_ip(cursor, bmc[key])
            if not bmc_output and not output:
                node = get_next_node_name(cursor)
                host_name = node + "." + domain_name

                modify_network_details.update_stanza_file(serial[key].lower(), node,
                                                          static_stanza_path)
                admin_ip = correlation_admin_bmc.correlation_bmc_to_admin(bmc[key],
                                                                          admin_subnet,
                                                                          netmask_bits)
                if admin_static_start_range <= admin_ip <= admin_static_end_range:
                    output = modify_network_details.check_presence_admin_ip(cursor, admin_ip)
                    if not output:
                        omniadb_connection.insert_node_info(serial[key], node,
                                                            host_name, None, admin_ip,
                                                            bmc[key], group_name, role, cluster_name,
                                                            PARENT, location_id, architecture,
                                                            DISCOVERY_MECHANISM, BMC_MODE, None,
                                                            None, None)
                    elif output:
                        admin_ip = modify_network_details.cal_uncorrelated_admin_ip(
                                                                cursor,
                                                                uncorrelated_admin_start_ip,
                                                                admin_static_start_range,
                                                                admin_static_end_range,
                                                                DISCOVERY_MECHANISM)
                        omniadb_connection.insert_node_info(serial[key], node, host_name, None,
                                                            admin_ip,bmc[key], group_name, role, cluster_name,
                                                            PARENT, location_id, architecture,
                                                            DISCOVERY_MECHANISM, BMC_MODE, None,
                                                            None, None)
                else:
                    admin_ip = modify_network_details.cal_uncorrelated_admin_ip(
                                                    cursor, uncorrelated_admin_start_ip,
                                                    admin_static_start_range,
                                                    admin_static_end_range,
                                                    DISCOVERY_MECHANISM)
                    omniadb_connection.insert_node_info(serial[key], node, host_name,
                                                        None, admin_ip,
                                                        bmc[key], group_name, role, cluster_name,
                                                         PARENT, location_id, architecture,
                                                        DISCOVERY_MECHANISM,
                                                        BMC_MODE, None, None, None)
            else:
                warnings.warn('Node already present in the database')
                print(serial[key])

        cursor.close()
        conn.close()


update_db()
