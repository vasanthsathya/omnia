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
Custom Ansible module to remove k8s lines from software.csv
if the given Kubernetes version is new (not recorded in metadata file).
"""

import os
from ansible.module_utils.basic import AnsibleModule
import yaml


def run_module():
    """
    Runs the Ansible module logic:
    - Checks if current_version is in metadata file.
    - If not, removes lines starting with 'k8s' from software.csv.
    """

    module_args = {
        "software_csv": {"type": "path", "required": True},
        "metadata_file": {"type": "path", "required": True},
        "current_version": {"type": "str", "required": True},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)

    software_csv = module.params["software_csv"]
    metadata_file = module.params["metadata_file"]
    current_version = module.params["current_version"]

    # Default: no changes
    changed = False

    # Check if files exist
    if not os.path.isfile(metadata_file) or not os.path.isfile(software_csv):
        module.exit_json(changed=False, msg="One or both files do not exist, nothing to do")

    # Load metadata yaml
    try:
        with open(metadata_file, encoding="utf-8") as metadata_file_obj:
            metadata = yaml.safe_load(metadata_file_obj)
    except yaml.YAMLError as err:
        module.fail_json(msg=f"Failed to parse metadata file: {err}")
    except OSError as err:
        module.fail_json(msg=f"Failed to read metadata file: {err}")

    versions = metadata.get("k8s_local_repo_versions", [])

    # If version already in metadata, nothing to do
    if current_version in versions:
        module.exit_json(changed=False, msg="K8s version already in metadata, nothing to do")

    # Else remove k8s line from software.csv
    try:
        with open(software_csv, "r", encoding="utf-8") as software_file_obj:
            lines = software_file_obj.readlines()
    except OSError as err:
        module.fail_json(msg=f"Failed to read software.csv: {err}")

    # Filter out lines starting with 'k8s' (like 'k8s.success')
    new_lines = [line for line in lines if not line.strip().startswith("k8s")]

    if len(new_lines) != len(lines):
        changed = True
        try:
            with open(software_csv, "w", encoding="utf-8") as software_file_obj:
                software_file_obj.writelines(new_lines)
        except OSError as err:
            module.fail_json(msg=f"Failed to write software.csv: {err}")

    module.exit_json(
        changed=changed,
        msg="k8s line removed from software.csv" if changed else "No k8s line to remove",
    )


def main():
    """Main entry point."""
    run_module()


if __name__ == "__main__":
    main()
