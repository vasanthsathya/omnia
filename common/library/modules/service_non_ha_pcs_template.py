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

"""
Generates non-HA PCS template.

This module is used to generate the template for non-HA PCS nodes.
It provides the necessary configuration and settings for the nodes.
"""

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.discovery.standard_functions import (
    create_directory,
    render_template,
    load_vars_file
)

def main():
    """
    The main function is the entry point of the Ansible module. It defines the module arguments, 
    creates the Ansible module, extracts the module parameters, loads the variables file, 
    and processes each node in the discovered_service_nodes list. The function creates the 
    node directories, loads the variables file, and renders the templates for corosync, pcs container, 
    and pcs start. The function returns a JSON object with the results of processing each node.

    Args:
        discovered_service_nodes (list): A list of dictionaries where each dictionary contains 
            the service_tag, hostname, and admin_ip.
        service_node_base_dir (str): The base directory where the service nodes will be created.
        file_permissions (str): The file permissions for the directories and files created.
        corosync_tmpl (str): The path to the corosync template.
        corosync_tmpl (str): The path to the pcs container template.
        pcs_start_tmpl (str): The path to the pcs start template.
        oim_shared_path (str): The path to the oim shared path.
        vars_file (str): The path to the variables file.

    Returns:
        A JSON object with the results of processing each node.
    """
    # Define the module arguments
    module_args = {
        "discovered_service_nodes": {"type": "list", "required": True},
        "service_node_base_dir": {"type": "str", "required": True},
        "file_permissions": {"type": "str", "required": True},
        "corosync_tmpl": {"type": "str", "required": True},
        "pcs_container_tmpl": {"type": "str", "required": True},
        "pcs_start_tmpl": {"type": "str", "required": True},
        "oim_shared_path": {"type": "str", "required": True},
        "vars_file": {"type": "str", "required": False, "default": None}
    }

    # Create the Ansible module
    module = AnsibleModule(argument_spec=module_args)

    # Extract the module parameters
    nodes = module.params['discovered_service_nodes']
    base_dir = module.params['service_node_base_dir']
    file_mode = int(module.params['file_permissions'], 8)
    tmpl_corosync = module.params['corosync_tmpl']
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

        # Create telemetry directories when idrac telemetry is supported
        # if module.params['idrac_telemetry_support'] == 'true':        
        telemetry_dir = os.path.join(service_dir, 'telemetry')
        idrac_telemetry_dir = os.path.join(telemetry_dir, 'idrac_telemetry')
        activemq_dir = os.path.join(idrac_telemetry_dir, 'activemq')
        mysql_dir = os.path.join(idrac_telemetry_dir, 'mysql')
        idrac_telemetry_receiver_dir = os.path.join(idrac_telemetry_dir, 'idrac_telemetry_receiver')
        prometheus_dir = os.path.join(telemetry_dir, 'prometheus')
        prometheus_pump_dir = os.path.join(telemetry_dir, 'prometheus_pump')

        log_dir = os.path.join(service_dir, 'log')
        telemetry_log_dir = os.path.join(log_dir, 'telemetry')
        activemq_log = os.path.join(telemetry_log_dir, 'activemq')
        mysql_log = os.path.join(telemetry_log_dir, 'mysql')
        idrac_telemetry_receiver_log = os.path.join(telemetry_log_dir, 'idrac_telemetry_receiver')
        prometheus_log = os.path.join(telemetry_log_dir, 'prometheus')
        prometheus_pump_log = os.path.join(telemetry_log_dir, 'prometheus_pump')

        # Create the directories
        for path in [
            service_dir, pcs_dir, pcs_config_dir, pcs_corosync_dir,
            telemetry_dir, idrac_telemetry_dir, activemq_dir, mysql_dir,
            idrac_telemetry_receiver_dir, prometheus_dir, prometheus_pump_dir,
            grafana_dir, loki_dir, log_dir, telemetry_log_dir, activemq_log,
            mysql_log, idrac_telemetry_receiver_log, prometheus_log,
            prometheus_pump_log
        ]:
            create_directory(path, file_mode)


        # Create the template context
        context = {
            'service_tag': service_tag,
            'service_node_name': service_node_name,
            'service_admin_nic_ip': service_admin_nic_ip,
            'oim_shared_path': oim_shared_path,
            **extra_vars
        }

        # Render the templates
        render_template(tmpl_corosync, corosync_path, context)
        render_template(tmpl_pcs_start, start_script_path, context)
        render_template(tmpl_pcs_container, container_path, context)

        os.chmod(start_script_path, file_mode)

        # Add the result to the list
        results.append(f"Processed node {service_tag}")

    # Exit the module
    module.exit_json(changed=True, msg="Nodes processed successfully", results=results)

if __name__ == '__main__':
    main()
