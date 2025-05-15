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
""" Ansible module to update BMC group entry in CSV file. """
import csv
import os
import requests
from requests.auth import HTTPBasicAuth
from ansible.module_utils.basic import AnsibleModule
from requests.exceptions import ConnectTimeout, HTTPError, ConnectionError, Timeout, RequestException
requests.packages.urllib3.disable_warnings()

def is_bmc_reachable_or_auth(ip, username, password, module):
    """
    Check if the BMC is reachable and if the credentials are valid.
    Returns True if reachable and authenticated, False otherwise.
    """
    url = f"https://{ip}/redfish/v1/"
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password),
            timeout=5,
            verify=False
        )

        if response.status_code == 200:
            return True
        if response.status_code == 401:
            module.warn(f"BMC IP {ip} is reachable, but bmc credential is invalid.")
            return False

        module.warn(f"BMC IP {ip} responded with unexpected status code: {response.status_code}")
        return False

    except ConnectTimeout:
        module.warn(f"BMC IP {ip} connection timed out. Not reachable.")
    except HTTPError as http_err:
        module.warn(f"BMC IP {ip} HTTP error occurred: {http_err}")
    except ConnectionError:
        module.warn(f"BMC IP {ip} is unreachable (connection error).")
    except Timeout:
        module.warn(f"BMC IP {ip} request timed out.")
    except RequestException as req_err:
        module.warn(f"BMC IP {ip} encountered a request error: {req_err}")

    return False

def read_entries_csv(csv_path, module):
    "Reading existing entries from the CSV file"
    entries = {}
    expected_columns = {'BMC_IP', 'GROUP_NAME', 'PARENT'}

    if os.path.exists(csv_path):
        try:
            with open(csv_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                actual_columns = set(reader.fieldnames or [])
                if not expected_columns.issubset(actual_columns):
                    module.fail_json(
                        msg=f"CSV file at {csv_path} is missing required columns. \
                            Expected: {expected_columns}, \
                            Found: {actual_columns}"
                    )

                for row in reader:
                    entries[row['BMC_IP']] = row
        except csv.Error as e:
            module.fail_json(msg=f"Failed to parse CSV file at {csv_path}: {str(e)}")
        except Exception as e:
            module.fail_json(msg=f"Unexpected error reading CSV at {csv_path}: {str(e)}")

    return entries


def write_entries_csv(csv_path, entries):
    "Writing BMC with group details entries to the CSV file"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['BMC_IP', 'GROUP_NAME', 'PARENT']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries.values():
            writer.writerow(entry)

def delete_bmc_entries(nodes, existing_entries, result):
    """
    Delete BMC entries from the existing entries based on the provided nodes.
    """
    for node in nodes:
        bmc_ip = node.get('bmc_ip')
        if bmc_ip in existing_entries:
            del existing_entries[bmc_ip]
            result['deleted'].append(bmc_ip)
            result['changed'] = True

def add_bmc_entries(nodes, existing_entries, bmc_username, bmc_password, module, result):
    """
    Add BMC entries to the existing entries based on the provided nodes.
    """
    for node in nodes:
        bmc_ip = node.get('bmc_ip')
        group = node.get('group_name', '')
        parent = node.get('parent', '')

        if bmc_ip and bmc_ip not in existing_entries:
            if is_bmc_reachable_or_auth(bmc_ip, bmc_username, bmc_password, module):
                existing_entries[bmc_ip] = {
                    'BMC_IP': bmc_ip,
                    'GROUP_NAME': group,
                    'PARENT': parent
                }
                result['added'].append(bmc_ip)
                result['changed'] = True
            else:
                result['invalid'].append(bmc_ip)
                result['changed'] = True



def main():
    "Main function for the custom ansible module - update_bmc_group_entry"
    module_args = dict(
        csv_path=dict(type='str', required=True),
        nodes=dict(type='list', elements='dict', required=True),
        bmc_username=dict(type='str', required=False, no_log=True),
        bmc_password=dict(type='str', required=False, no_log=True),
        delete=dict(type='bool', default=False)
    )

    result = dict(changed=False, added=[], deleted=[], invalid=[])

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    csv_path = module.params['csv_path']
    nodes = module.params['nodes']
    delete = module.params['delete']
    bmc_username = module.params['bmc_username']
    bmc_password = module.params['bmc_password']

    # Validate username and password only if delete is False
    if not delete and (not bmc_username or not bmc_password):
        module.fail_json(msg="bmc_username and bmc_password are mandatory for add operation.")

    existing_entries = read_entries_csv(csv_path, module)

    if delete:
        delete_bmc_entries(nodes, existing_entries, result)
    else:
        add_bmc_entries(nodes, existing_entries, bmc_username, bmc_password, module, result)

    write_entries_csv(csv_path, existing_entries)
    module.exit_json(**result)

if __name__ == '__main__':
    main()
