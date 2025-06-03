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
import shutil


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.discovery.standard_functions import (
    create_directory,
    render_template,
    load_vars_file
)


def main():

    module_args = {
        "service_ha_data": {"type": "dict", "required": True},
        "service_node_base_dir": {"type": "str", "required": True},
        "file_permissions": {"type": "str", "required": True},
        "corosync_tmpl": {"type": "str", "required": True},
        "pcs_container_tmpl": {"type": "str", "required": True},
        "pcs_start_tmpl": {"type": "str", "required": True},
        "oim_shared_path": {"type": "str", "required": True},
        "admin_netmask": {"type": "str", "required": True},
        "vars_file": {"type": "str", "required": False, "default": None}
    }

    module = AnsibleModule(argument_spec=module_args)

    ha_data = module.params['service_ha_data']
    base_dir = module.params['service_node_base_dir']
    file_mode = int(module.params['file_permissions'], 8)
    tmpl_corosync = module.params['corosync_tmpl']
    tmpl_pcs_container = module.params['pcs_container_tmpl']
    tmpl_pcs_start = module.params['pcs_start_tmpl']
    oim_path = module.params['oim_shared_path']
    vars_file = module.params['vars_file']
    admin_netmask = module.params['admin_netmask']

    extra_vars = load_vars_file(vars_file)

    results = []

    for _, nodes in ha_data.items():
        active_node = next((n for n in nodes if n.get('active')), None)
        passive_nodes = [n for n in nodes if not n.get('active')]

        if not active_node:
            continue

        service_tag = active_node['service_tag']
        service_tag_dir = os.path.join(base_dir, service_tag)
        pcs_dir = os.path.join(service_tag_dir, 'pcs')
        pcs_config_dir = os.path.join(pcs_dir, 'config')
        pcs_corosync_dir = os.path.join(pcs_dir, 'corosync')
        container_path = os.path.join(pcs_dir, 'omnia_pcs.container')
        start_script_path = os.path.join(pcs_config_dir, 'pcs-start.sh')
        corosync_path = os.path.join(pcs_corosync_dir, 'corosync.conf')

        # Create telemetry directories when idrac telemetry is supported
        # if module.params['idrac_telemetry_support'] == 'true':
        telemetry_dir = os.path.join(service_tag_dir, 'telemetry')
        idrac_telemetry_dir = os.path.join(telemetry_dir, 'idrac_telemetry')
        activemq_dir = os.path.join(idrac_telemetry_dir, 'activemq')
        mysql_dir = os.path.join(idrac_telemetry_dir, 'mysql')
        idrac_telemetry_receiver_dir = os.path.join(idrac_telemetry_dir, 'idrac_telemetry_receiver')
        prometheus_dir = os.path.join(telemetry_dir, 'prometheus')
        prometheus_pump_dir = os.path.join(telemetry_dir, 'prometheus_pump')

        log_dir = os.path.join(service_tag_dir, 'log')
        telemetry_log_dir = os.path.join(log_dir, 'telemetry')
        activemq_log = os.path.join(telemetry_log_dir, 'activemq')
        mysql_log = os.path.join(telemetry_log_dir, 'mysql')
        idrac_telemetry_receiver_log = os.path.join(telemetry_log_dir, 'idrac_telemetry_receiver')
        prometheus_log = os.path.join(telemetry_log_dir, 'prometheus')
        prometheus_pump_log = os.path.join(telemetry_log_dir, 'prometheus_pump')

        for d in [
            service_tag_dir, pcs_dir, pcs_config_dir, pcs_corosync_dir,telemetry_dir,
            idrac_telemetry_dir, activemq_dir, mysql_dir, idrac_telemetry_receiver_dir,
            prometheus_dir, prometheus_pump_dir, log_dir, telemetry_log_dir,
            activemq_log, mysql_log, idrac_telemetry_receiver_log, prometheus_log, prometheus_pump_log
        ]:
            create_directory(d, file_mode)

        context = {
            'service_tag': service_tag,
            'active_node': active_node,
            'passive_nodes': passive_nodes,
            'oim_shared_path': oim_path,
            'admin_netmask': admin_netmask,
            **extra_vars
        }

        render_template(tmpl_corosync, corosync_path, context)
        render_template(tmpl_pcs_container, container_path, context)
        render_template(tmpl_pcs_start, start_script_path, context)

        os.chmod(start_script_path, file_mode)

        results.append(f"Configured HA group: {service_tag}")

        # Copy rendered active node directory to passive node directories
        for p_node in passive_nodes:
            passive_service_tag = p_node['service_tag']
            passive_service_tag_dir = os.path.join(base_dir, passive_service_tag)

            if os.path.exists(passive_service_tag_dir):
                shutil.rmtree(passive_service_tag_dir)

            shutil.copytree(service_tag_dir, passive_service_tag_dir)
            results.append(f"Copied config from active node: {service_tag} to passive node: {passive_service_tag}")

    module.exit_json(changed=True, msg="Service node configurations rendered.", results=results)


if __name__ == '__main__':
    main()
