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
    parent_tags = set()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            parent = row.get('PARENT', '').strip()
            if parent:
                parent_tags.add(parent)
    return parent_tags



def fetch_admin_ip(parent_tags, service_node_metadata):
    """Validates input against rules."""
    service_node_admin_ip = {}
    for service_tag,data in service_node_metadata.items():
        if service_tag in parent_tags:
            service_node_admin_ip[service_tag] = data['admin_ip']
    return service_node_admin_ip


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
        sn_admin_ip = fetch_admin_ip(parent_tags, service_node_metadata)
        module.exit_json(changed=False, sn_admin_ip=sn_admin_ip)
    except ValueError as e:
        module.fail_json(msg=f"Failed to to get Service Node Group data. {e}")

if __name__ == "__main__":
    main()
