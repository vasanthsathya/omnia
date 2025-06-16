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

#!/usr/bin/python3
"""
Ansible module to remove specified software entries from a CSV file.
"""

import os
import csv
from ansible.module_utils.basic import AnsibleModule

def run_module():
    """
    Run the Ansible module to remove software entries from a CSV file.

    Parameters:
        None

    Returns:
        None
    """
    module_args = {
        "csv_path": {"type": "path", "required": True},
        "softwares": {
            "type": "list",
            "elements": "str",
            "required": True
        }
    }

    module = AnsibleModule(argument_spec=module_args)

    csv_path = module.params["csv_path"]
    softwares = module.params["softwares"]
    changed = False

    if not os.path.exists(csv_path):
        module.fail_json(msg=f"{csv_path} does not exist")

    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            lines = list(csv.reader(f))
    except (OSError, csv.Error) as e:
        module.fail_json(msg=f"Failed to read CSV file: {e}")

    if not lines:
        module.exit_json(changed=False, msg="CSV file is empty")

    header = lines[0]
    data = lines[1:]

    new_data = [row for row in data if row[0].strip() not in softwares]

    if len(new_data) != len(data):
        changed = True
        try:
            with open(csv_path, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(new_data)
        except (OSError, csv.Error) as e:
            module.fail_json(msg=f"Failed to write CSV file: {e}")

    module.exit_json(
        changed=changed,
        msg=f"Removed: {softwares}" if changed else "No matching software found"
    )

def main():
    """Entry point for module execution."""
    run_module()

if __name__ == "__main__":
    main()
