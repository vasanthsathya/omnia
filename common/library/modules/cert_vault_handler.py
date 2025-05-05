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
import os
import stat
import secrets
import string
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.local_repo.standard_logger import setup_standard_logger
from ansible.module_utils.local_repo.common_functions import process_file, load_yaml_file
from ansible.module_utils.local_repo.config import (
    USER_REPO_URL,
    LOCAL_REPO_CONFIG_PATH_DEFAULT,
    VAULT_KEY_PATH
)

def extract_repos_with_certs(repo_entries, log):
    """
    Extracts repositories that include SSL certificate configuration.

    Args:
        repo_entries (list): List of dictionaries with possible keys:
                             'name', 'sslcacert', 'sslclientkey', 'sslclientcert'.

    Returns:
        list: A list of dictionaries, each containing 'name', 'sslcacert',
              'sslclientkey', and 'sslclientcert' for repos where 'sslcacert' is present.
    """
    results = []

    for entry in repo_entries:
        if "sslcacert" in entry and entry["sslcacert"]:
            results.append({
                "name": entry.get("name", "unknown"),
                "sslcacert": entry["sslcacert"],
                "sslclientkey": entry.get("sslclientkey", ""),
                "sslclientcert": entry.get("sslclientcert", "")
            })
    log.info(f"Appended result with number of entries: {len(results)}")
    return results

def generate_vault_key(module, key_path, log):
    """
    Generate a secure Ansible Vault key only if the file does not exist

    Args:
        module (AnsibleModule): The active Ansible module object.
        key_path (str): The path where the Vault key file should be saved.

    Returns:
        bool: True if key was created, False otherwise.
    """
    if os.path.isfile(key_path):
        log.info("Ansible Vault key for user repo already exist")
        return True

    try:
        os.makedirs(os.path.dirname(key_path), exist_ok=True)

        alphabet = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(alphabet) for _ in range(32))

        with open(key_path, "w", encoding = "utf-8") as f:
            f.write(key + "\n")

        os.chmod(key_path, stat.S_IRUSR | stat.S_IWUSR)
        log.info("Ansible Vault key for user repo created")
        return True
    except Exception as e:
        module.fail_json(msg=f"Failed to generate vault key: {str(e)}")
        return False

def main():
    """
    Encrypt or decrypt files using Ansible Vault.

    The module takes in the following parameters:
        * file_path: The path to the file to encrypt or decrypt.
        * dir_path: The path to the directory containing files to encrypt or decrypt.
        * vault_key: The path to the Ansible Vault key.
        * mode: The mode of operation, either 'encrypt' or 'decrypt'.

    The module is mutually exclusive for file_path and dir_path.
    The module requires one of file_path or dir_path.
    The module does not support check mode.
    """
    module = AnsibleModule(
    argument_spec={
        'mode': {'type': 'str', 'required': True, 'choices': ['encrypt', 'decrypt']},
        'log_dir': {'type': 'str', 'required': False, 'default': '/tmp/thread_logs'}
    },
    supports_check_mode=False
    )
    mode = module.params['mode']
    log_dir = module.params["log_dir"]

    log = setup_standard_logger(log_dir)

    start_time = datetime.now().strftime("%I:%M:%S %p")

    log.info(f"Start execution time cert_vault_handler: {start_time}")


    local_repo_config = load_yaml_file(LOCAL_REPO_CONFIG_PATH_DEFAULT)
    user_repos = local_repo_config.get(USER_REPO_URL, [])
    if not user_repos:
        log.info(f"No user repo found, proceeding without encryption")
        module.exit_json()

    cert_entries = extract_repos_with_certs(user_repos, log)
    for entry in cert_entries:
        for key in ["sslcacert", "sslclientkey", "sslclientcert"]:
            path = entry.get(key)
            if path and not os.path.isfile(path):
                module.fail_json(msg=f"Missing {key} for repo '{entry['name']}': {path}")

    messages = []
    changed = False

    if cert_entries:
        generate_vault_key(module, VAULT_KEY_PATH, log)
        log.info(f"User repo found, proceeding to encrypt")
        for entry in cert_entries:
            for key in ["sslcacert", "sslclientkey", "sslclientcert"]:
                path = entry.get(key)
                if path:
                    result, msg = process_file(path, VAULT_KEY_PATH, mode)
                    if result is False:
                        module.fail_json(msg=f"Failed to {mode} {key} for '{entry['name']}': {msg}")
                    else:
                        messages.append(msg)
                        changed = True

    module.exit_json(changed=changed, msg="; ".join(messages))

if __name__ == '__main__':
    main()
