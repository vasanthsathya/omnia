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

"""
Ansible custom module to append 'ip=<ip>' to each relevant line in the inventory file.
It reads the `src` file, appends `ip=` for matching IPs or ansible_host values,
and writes the result to `dest`.
"""

import re

from ansible.module_utils.basic import AnsibleModule


def run_module():
    """Main module logic."""
    module_args = {
        "src": {"type": "str", "required": True},
        "dest": {"type": "str", "required": True},
    }

    result = {
        "changed": False,
        "original_file": "",
        "updated_file": "",
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
    )

    src = module.params["src"]
    dest = module.params["dest"]
    result["original_file"] = src
    result["updated_file"] = dest

    try:
        with open(src, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, IOError) as e:
        module.fail_json(msg=f"Failed to read source file: {e}", **result)

    updated_lines = []

    for line in lines:
        stripped = line.strip()

        # Leave headers and blank lines unchanged
        if not stripped or stripped.startswith("["):
            updated_lines.append(line)
            continue

        # Line with ansible_host
        match_ansible = re.search(r"ansible_host=(\d+\.\d+\.\d+\.\d+)", line)
        if match_ansible:
            ip = match_ansible.group(1)
            if f"ip={ip}" not in line:
                line = line.rstrip() + f" ip={ip}\n"
                result["changed"] = True
            updated_lines.append(line)
            continue

        # Line that is just an IP
        match_ip = re.match(r"^(\d+\.\d+\.\d+\.\d+)$", stripped)
        if match_ip:
            ip = match_ip.group(1)
            updated_lines.append(f"{ip} ip={ip}\n")
            result["changed"] = True
            continue

        # Leave unchanged
        updated_lines.append(line)

    try:
        with open(dest, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
    except (OSError, IOError) as e:
        module.fail_json(msg=f"Failed to write destination file: {e}", **result)

    module.exit_json(**result)


def main():
    """Entry point for module execution."""
    run_module()


if __name__ == "__main__":
    main()
