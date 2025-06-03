#  Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
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

# pylint: disable=import-error,no-name-in-module,line-too-long

#!/usr/bin/python

"""Ansible module to update BMC subnet routes for a Service Node."""

import subprocess
import ipaddress
import json
from ansible.module_utils.basic import AnsibleModule

module = AnsibleModule(
        argument_spec={
            'oim_nic': {'required': True, 'type': 'str'},
            'oim_nic_ip': {'required': True, 'type': 'str'},
            'oim_nic_netmask_bits': {'required': True, 'type': 'str'},
            'servicetag': {'required': True, 'type': 'str'},
            'all_nodes': {'required': True, 'type': 'list'},
            'delete': {'required': False, 'type': 'bool', 'default': False},
        },
        supports_check_mode=True
    )

nic = module.params['oim_nic']
oim_nic_ip = module.params['oim_nic_ip']
netmask_bits = module.params['oim_nic_netmask']
servicetag = module.params['servicetag']
all_nodes = module.params['all_nodes']

def ping_host(ip):
    """Ping a host to check if it is reachable."""
    try:
        subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_existing_routes():
    """Get existing routes from the kernel route table."""
    try:
        output = subprocess.check_output(['ip', '-j', 'route']).decode()
        routes = json.loads(output)
        return [route['dst'] for route in routes if 'dst' in route]
    except Exception:
        return []


def route_exists(subnet, existing_routes):
    """Check if a route exists in the existing routes for the specified subnet."""
    try:
        target_net = ipaddress.ip_network(subnet)
        for route in existing_routes:
            route_net = ipaddress.ip_network(route, strict=False)
            if target_net.subnet_of(route_net):
                return True
        return False
    except ValueError:
        return False


def route_exists_in_nmcli(subnet):
    """Check if a route exists in nmcli for the specified subnet."""
    try:
        output = subprocess.check_output(['nmcli', 'connection', 'show', nic], text=True)
        return subnet in output
    except subprocess.CalledProcessError:
        return False


def add_route_nmcli(subnet):
    """Add a route to the specified subnet using nmcli."""
    try:
        subprocess.check_call(['nmcli', 'connection', 'modify', nic, '+ipv4.routes', subnet])
        subprocess.check_call(['nmcli', 'connection', 'up', nic])
        return True
    except subprocess.CalledProcessError:
        return False

def delete_route_nmcli(subnet):
    """Delete a route using nmcli."""
    try:
        subprocess.check_call(['nmcli', 'connection', 'modify', nic, '-ipv4.routes', subnet])
        subprocess.check_call(['nmcli', 'connection', 'up', nic])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Main function to update BMC subnet routes for a Service Node."""

    bmc_ips = [
        n['bmc_ip'] for n in all_nodes
        if n.get('parent') == servicetag and n.get('bmc_ip')
    ]

    if not bmc_ips:
        module.warn(f"No Compute nodes with BMC IPs found for this Service Node - ({servicetag}).")
        module.exit_json(changed=False, skipped=True, servicetag=servicetag)

    subnets = set()
    for ip in bmc_ips:
        net = ipaddress.ip_network(f"{ip}/{netmask_bits}", strict=False)
        if not ping_host(ip):
            subnets.add(str(net))
        else:
            module.warn(f"BMC IP {ip} is reachable, skipping subnet addition.")

    existing_routes = get_existing_routes()
    if not existing_routes:
        module.warn(f"No routes found in kernel route table. Service Node ({servicetag}) may be misconfigured.")
        module.exit_json(changed=False, skipped=True, servicetag=servicetag)

    added = []
    unreachable_nodes = []

    for subnet in subnets:
        if route_exists(subnet, existing_routes) or route_exists_in_nmcli(subnet):
            continue
        subnet_gateway = f"{subnet} {oim_nic_ip}"
        if add_route_nmcli(subnet_gateway):
            added.append(subnet_gateway)

    for ip in bmc_ips:
        if not ping_host(ip):
            unreachable_nodes.append(ip)

    result = {
        "changed": bool(added),
        "added_routes": added,
        "unreachable_bmc": unreachable_nodes,
        "servicetag": servicetag,
    }

    if unreachable_nodes:
        module.warn(f"The following BMC IPs are still unreachable: {unreachable_nodes}")

    module.exit_json(**result)


if __name__ == '__main__':
    main()
