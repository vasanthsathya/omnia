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

#!/usr/bin/python

""" This module is used to fetch telemetry host inventory"""

import csv
from ansible.module_utils.basic import AnsibleModule

def fetch_parent_tags(file_path):
    """
    This function fetches the parent tags from a given CSV file.

    Parameters:
        file_path (str): The path to the CSV file containing parent tags.

    Returns:
        set: A set of parent tags found in the CSV file.
    """
    parent_tags = set()    
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parent = row.get('PARENT', '').strip()
            if parent:
                parent_tags.add(parent)
    return parent_tags



def fetch_admin_ip(parent_tags, service_node_metadata):
    """
    Fetches the admin IP and virtual IP addresses of service nodes based on the provided parent tags and service node metadata.

    Parameters:
        parent_tags (list): A list of parent tags used to identify service nodes.
        service_node_metadata (dict): A dictionary containing metadata about service nodes, including admin IP and virtual IP addresses.

    Returns:
        tuple: A tuple containing two dictionaries. The first dictionary maps service tags to their corresponding admin IP addresses.
               The second dictionary maps service tags to their corresponding virtual IP addresses.
    """
    service_node_admin_ip = {}
    service_node_active_ip = {}
    active_nodes, passive_nodes, ha_status = fetch_active_passive_servicetags(
        parent_tags, service_node_metadata)
    for nodes in (active_nodes, passive_nodes):
        for service_tag in nodes:
            service_node_admin_ip[service_tag] = service_node_metadata[service_tag]['admin_ip']

    for service_tag in active_nodes:
        if ha_status:
            service_node_active_ip[service_tag] = \
                service_node_metadata[service_tag]['virtual_ip_address']
        else:
            service_node_active_ip[service_tag] = \
                service_node_metadata[service_tag]['admin_ip']

    return service_node_admin_ip, service_node_active_ip

def fetch_active_passive_servicetags(parent_tags, service_node_metadata):
    """
    Fetches the active and passive service tags based 
    on the provided parent tags and service node metadata.

    Parameters:
        parent_tags (list): A list of parent tags used to identify service nodes.
        service_node_metadata (dict): A dictionary containing metadata about service nodes.

    Returns:
        tuple: A tuple containing two sets. The first set contains active service tags.
               The second set contains passive service tags.
    """
    ha_status = False
    active_nodes = set()
    passive_nodes = set()
    for service_tag, data in service_node_metadata.items():
        if service_tag in parent_tags:
            if data['enable_service_ha']:
                ha_status = True
                if data['active']:
                    active_nodes.add(service_tag)
                    passive_nodes.update(data['passive_nodes'])
                else:
                    passive_nodes.add(service_tag)
            else:
                active_nodes.add(service_tag)
    return active_nodes, passive_nodes, ha_status

def main():
    """Main module function."""
    module_args = dict(
        bmc_group_data_path=dict(type="str", required=True),
        service_node_metadata=dict(type="dict", required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    bmc_group_data_path = module.params["bmc_group_data_path"]
    service_node_metadata = module.params["service_node_metadata"]
    try:
        parent_tags = fetch_parent_tags(bmc_group_data_path)
        sn_admin_ip, sn_active_ip = fetch_admin_ip(parent_tags, service_node_metadata)
        module.exit_json(changed=False, sn_admin_ip=sn_admin_ip, sn_active_ip=sn_active_ip)
    except ValueError as e:
        module.fail_json(msg=f"Failed to to get Service Node Group data. {e}")

if __name__ == "__main__":
    main()
