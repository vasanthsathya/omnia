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

#!/usr/bin/python

# pylint: disable=import-error,no-name-in-module,line-too-long

import sys
import yaml
import json
import os
import traceback

import ansible.module_utils.discovery.omniadb_connection as omniadb

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.discovery.standard_functions import load_vars_file


def get_node_summary(service_tag):
    """
    Fetches node details for a given service tag from the database.

    Args:
        service_tag (str): The service tag to query for node details.

    Returns:
        dict: A dictionary containing the node details, including service_tag, node, hostname, and admin_ip. If the query fails, it returns an error message.
    """
    try:
        conn = omniadb.create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT service_tag, node, hostname, admin_ip FROM cluster.nodeinfo WHERE service_tag = %s",
            (service_tag,)
        )
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        if records:
            node = records[0]
            return {
                "service_tag": node[0],
                "node": node[1],
                "hostname": node[2],
                "admin_ip": node[3]
            }
    except Exception as e:
        return {"error": f"DB query failed for service tag '{service_tag}': {e}"}
    return {}

def main():
    """
    The main function is the entry point of the Ansible module. It defines the module arguments, 
    creates the Ansible module, extracts the module parameters, loads the variables file, 
    and processes each node in the discovered_service_nodes list. The function creates the 
    node directories, loads the variables file, and renders the templates for corosync, pcs container, 
    and pcs start. The function returns a JSON object with the results of processing each node.

    Parameters:
        high_availability_config_path (str): The path to the high availability config file.
        service_node_base_dir (str): The base directory where the service nodes will be created.

    Returns:
        A JSON object with the results of processing each node, including the changed status, 
        a message describing the result, and the path to the written file.
    """
    module_args = dict(
        high_availability_config_path=dict(type='str', required=True),
        service_node_base_dir=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        msg="",
        written_file=""
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    ha_config_path = module.params['high_availability_config_path']
    base_dir = module.params['service_node_base_dir']

    try:
        data =load_vars_file(ha_config_path)

        if not data:
            module.fail_json(msg=f"No content found in {ha_config_path}. Please check the file.")

        results = {}
        ha = data.get('service_node_ha', {})

        if not isinstance(ha, dict):
            module.fail_json(msg="Invalid structure for 'service_node_ha'. It must be a dictionary.")

        if not ha.get('enable_service_ha'):
            result['msg'] = "Service HA is disabled in config."
            module.exit_json(**result)

        service_nodes = ha.get('service_nodes', [])
        if not service_nodes:
            module.fail_json(msg="No 'service_nodes' found in service_node_ha.")

        for node in service_nodes:
            vip = node.get('virtual_ip_address', '')
            active_service_tag = node.get('active_node_service_tag', '')
            passive_nodes_nested = node.get('passive_nodes', [])

            # Active node
            active_service_tag_info = get_node_summary(active_service_tag)
            if not active_service_tag_info or "error" in active_service_tag_info:
                continue

            active_service_tag_info.update({
                'virtual_ip': vip,
                'active': True
            })

            # Passive nodes
            passive_info_grouped = []
            for group in passive_nodes_nested:
                tags = group.get('node_service_tags', [])
                if not isinstance(tags, list):
                    continue
                for tag in tags:
                    passive_info = get_node_summary(tag)
                    if passive_info and "error" not in passive_info:
                        passive_info.update({
                            'virtual_ip': vip,
                            'active': False
                        })
                        passive_info_grouped.append(passive_info)

            node_key = active_service_tag_info['service_tag']
            node_data = [active_service_tag_info] + passive_info_grouped
            results[node_key] = node_data

        if not results:
            module.fail_json(msg="No valid service HA data found.")

        os.makedirs(base_dir, exist_ok=True)
        output_file_path = os.path.join(base_dir, 'service_ha_config_data.json')

        with open(output_file_path, 'w', encoding='utf-8') as outfile:
            json.dump(results, outfile, indent=4)

        result['changed'] = True
        result['msg'] = "Service HA config successfully written."
        result['written_file'] = output_file_path
        module.exit_json(**result)

    except yaml.YAMLError as e:
        module.fail_json(msg=f"YAML error: {str(e)}")
    except Exception:
        module.fail_json(msg="Unexpected error occurred", exception=traceback.format_exc())

if __name__ == '__main__':
    main()
