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

def check_service_node_entry(roles_config):
    roles_config_json = load_yaml(roles_config)

    roles_configured = roles_config_json.get('Roles',[])

    return next((role for role in roles_configured if role.get('name') == "service_node"), None)

def check_and_get_service_nodes_status(bmc_group_data_path, service_nodes_not_booted, service_nodes_booted):
    nodes_not_booted = []
    role = "service_node"
    conn = omniadb.create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT bmc_ip, status FROM cluster.nodeinfo WHERE role = %s",
            (role,)
    )
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    if records:
        records_dict = dict(records)
        with open(bmc_group_data_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bmc_ip = row.get('BMC_IP', '').strip()
                node_status = records_dict.get(bmc_ip)

                if node_status is not None and node_status != "booted":
                    service_nodes_not_booted.append(bmc_ip)
                elif node_status is not None and node_status == "booted":
                    service_nodes_booted.append(bmc_ip)

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

        roles_config = input_dir + "/roles_config.py"
        service_node_defined = check_service_node_entry(roles_config)

        if service_node_defined:
            check_and_get_service_nodes_status(bmc_group_data_path, service_nodes_not_booted, service_nodes_booted)

        module.exit_json(changed=False, service_node_defined=service_node_defined,
                         service_nodes_not_booted=service_nodes_not_booted, service_nodes_booted=service_nodes_booted)
    except ValueError as e:
        module.fail_json(msg=f"Failed to to get Service Node Group data. {e}")

if __name__ == "__main__":
    main()