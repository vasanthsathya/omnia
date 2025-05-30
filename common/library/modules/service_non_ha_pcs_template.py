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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.discovery.standard_functions import (
    create_directory,
    render_template,
    load_vars_file
)

import os

def main():
    # Define the module arguments
    module_args = dict(
        discovered_service_nodes=dict(type='list', required=True),
        service_node_base_dir=dict(type='str', required=True),
        file_permissions=dict(type='str', required=True),
        corosync_non_ha_tmpl=dict(type='str', required=True),
        pcs_container_tmpl=dict(type='str', required=True),
        pcs_start_tmpl=dict(type='str', required=True),
        oim_shared_path=dict(type='str', required=True),
        vars_file=dict(type='str', required=False, default=None)
    )

    # Create the Ansible module
    module = AnsibleModule(argument_spec=module_args)

    # Extract the module parameters
    nodes = module.params['discovered_service_nodes']
    base_dir = module.params['service_node_base_dir']
    perms = int(module.params['file_permissions'], 8)
    tmpl_corosync = module.params['corosync_non_ha_tmpl']
    tmpl_pcs_container = module.params['pcs_container_tmpl']
    tmpl_pcs_start = module.params['pcs_start_tmpl']
    oim_shared_path = module.params['oim_shared_path']
    vars_file = module.params['vars_file']

    # Load the variables file
    extra_vars = load_vars_file(vars_file)

    # Initialize the results list
    results = []

    # Process each node
    for node in nodes:
        # Extract the node parameters
        service_tag = node['service_tag']
        service_node_name = node['hostname']
        service_admin_nic_ip = node['admin_ip']

        # Create the node directories
        service_dir = os.path.join(base_dir, service_tag)
        pcs_dir = os.path.join(service_dir, 'pcs')
        pcs_config_dir = os.path.join(pcs_dir, 'config')
        pcs_corosync_dir = os.path.join(pcs_dir, 'corosync')
        container_path = os.path.join(pcs_dir, 'omnia_pcs.container')
        start_script_path = os.path.join(pcs_config_dir, 'pcs-start.sh')
        corosync_path = os.path.join(pcs_corosync_dir, 'corosync.conf')

        # Create the directories
        for path in [service_dir, pcs_dir, pcs_config_dir, pcs_corosync_dir]:
            create_directory(path, perms)

        # Create the template context
        context = {
            'service_tag': service_tag,
            'service_node_name': service_node_name,
            'service_admin_nic_ip': service_admin_nic_ip,
            'oim_shared_path': oim_shared_path,
            **extra_vars
        }

        # Render the templates
        render_template(tmpl_corosync, corosync_path, context, module)
        render_template(tmpl_pcs_start, start_script_path, context, module)
        render_template(tmpl_pcs_container, container_path, context, module)

        # Add the result to the list
        results.append(f"Processed node {service_tag}")

    # Exit the module
    module.exit_json(changed=True, msg="Nodes processed successfully", results=results)

if __name__ == '__main__':
    main()

