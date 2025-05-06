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

import json
import os
from ansible.module_utils.input_validation.common_utils import validation_utils
from ansible.module_utils.input_validation.common_utils import config
from ansible.module_utils.input_validation.common_utils import en_us_validation_msg

file_names = config.files
create_error_msg = validation_utils.create_error_msg
create_file_path = validation_utils.create_file_path

# Below is a validation function for each file in the input folder
def validate_local_repo_config(input_file_path, data, logger, module, omnia_base_dir, module_utils_base, project_name):
    # check to make sure associated os info is filled out
    errors = []
    software_config_file_path = create_file_path(input_file_path, file_names["software_config"])
    software_config_json = json.load(open(software_config_file_path, "r"))
    cluster_os_type = software_config_json["cluster_os_type"]
    omnia_repo_url_rhel = data["omnia_repo_url_rhel"]

    rhel_os_url = data["rhel_os_url"]
    oim_os = validation_utils.get_os_type()
    if cluster_os_type.lower() == "rhel" and oim_os.lower() == cluster_os_type.lower():
        if validation_utils.is_string_empty(rhel_os_url):
            errors.append(create_error_msg("rhel_os_url", rhel_os_url, en_us_validation_msg.rhel_os_url_msg))
    elif oim_os.lower() != cluster_os_type.lower():
        errors.append(create_error_msg(input_file_path, oim_os , "The cluster OS mentioned in software config does not match the OIM OS"))

    return errors
