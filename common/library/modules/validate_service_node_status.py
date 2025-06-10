# Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=import-error

#!/usr/bin/python

""" This module is used to fetch telemetry host inventory"""

import csv
import os
import yaml
import ansible.module_utils.discovery.omniadb_connection as omniadb

from ansible.module_utils.basic import AnsibleModule

def load_yaml(path):
    """
    Load YAML from a given file path.

    Args:
        path (str): The path to the YAML file.

    Returns:
        dict: The loaded YAML data.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding = "utf-8") as file:
        return yaml.safe_load(file)

def is_service_node_defined(roles_config):
    """
    Checks if a 'service_node' entry exists in the roles configuration.

    Args:
        roles_config (str): The path to the roles configuration file.

    Returns:
        bool: True if a 'service_node' entry is found, False otherwise.

    Notes:
        This function loads the roles configuration from the specified file and checks
        for the presence of a 'service_node' role.
    """

    roles_config_json = load_yaml(roles_config)

    roles_configured = roles_config_json.get('Roles',[])

    return any(role.get('name') == "service_node" for role in roles_configured)


def check_and_get_service_nodes_status(
    bmc_group_data_path,
    service_nodes_not_booted,
    service_nodes_booted,
    module
):
    """
    Checks the status of service nodes and updates the lists of booted and not booted nodes.

    This function queries the database for the status of service nodes,
    reads the BMC group data from a file,
    and updates the lists of booted and not booted service nodes based on the node status.

    Args:
        bmc_group_data_path (str): The path to the BMC group data file.
        service_nodes_not_booted (list): A list to store the BMC IPs of service nodes
                                        that are not booted.
        service_nodes_booted (list): A list to store the BMC IPs of service nodes that are booted.

    Returns:
        None

    Notes:
        This function assumes that the database connection is established and
        the BMC group data file is in the correct format.
        The function updates the input lists `service_nodes_not_booted` and `service_nodes_booted`
        with the BMC IPs of service nodes that are not booted and booted, respectively.
    """

    try:
        role = "service_node"
        conn = omniadb.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT bmc_ip, status FROM cluster.nodeinfo WHERE role = %s",
                (role,)
            )
            records = cursor.fetchall()
        except Exception as e:
            print(f"Error: Failed to execute query. {e}")
            return
        finally:
            cursor.close()
            conn.close()

        if records:
            records_dict = {record[0]: record[1] for record in records}
            try:
                with open(bmc_group_data_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        bmc_ip = row.get('BMC_IP', '').strip()
                        node_status = records_dict.get(bmc_ip)

                        if node_status is not None and node_status != "booted":
                            service_nodes_not_booted.append(bmc_ip)
                        elif node_status is not None and node_status == "booted":
                            service_nodes_booted.append(bmc_ip)
            except FileNotFoundError:
                module.fail_json(msg="File {%s} not found" % (bmc_group_data_path))
            except csv.Error as e:
                module.fail_json(msg=f"Error: Failed to read file '{bmc_group_data_path}'. {e}")
    except Exception as e:
        module.warn(f"Error: Failed to create database connection. {e}")

def main():
    """Main module function."""
    module_args = {
        'input_dir': {'type': "str", 'required': True},
        'bmc_group_data_path': {'type': "str", 'required': True},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    input_dir = module.params["input_dir"]
    bmc_group_data_path = module.params["bmc_group_data_path"]

    service_nodes_not_booted = []
    service_nodes_booted = []
    service_node_defined = False

    try:

        roles_config = input_dir + "/roles_config.yml"
        service_node_defined = is_service_node_defined(roles_config)

        if service_node_defined:
            check_and_get_service_nodes_status(bmc_group_data_path,
                                               service_nodes_not_booted,
                                               service_nodes_booted, module)

        module.exit_json(changed=False,
                         service_node_defined=service_node_defined,
                         service_nodes_not_booted=service_nodes_not_booted,
                         service_nodes_booted=service_nodes_booted)
    except ValueError as e:
        module.fail_json(msg=f"Failed to to get Service Node data. {e}")

if __name__ == "__main__":
    main()
