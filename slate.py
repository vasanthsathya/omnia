import json
import yaml
import copy
from pprint import pprint

RPM_LIST_BASE = "rpm"
REBOOT_KEY = "reboot"

# Read JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Read YAML file
def read_roles_config(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    role_cfg = {item['name']: item['groups'] for item in data.get('Roles', [])}
    return role_cfg

def careful_merge(split_dict, split_key, value):
    val_d = split_dict.get(split_key, {})
    # import pdb; pdb.set_trace()
    for key, val in value.items():
        if key == REBOOT_KEY:
            val_d[key] = val_d.get(key, False) or val
            continue
        got_existing_list = val_d.get(key, []) + val
        # Order matters?
        val_d[key] = list(set(got_existing_list)) # remove duplicates 
    split_dict[split_key] = val_d

def split_comma_keys(input_dict):
    split_dict = {}
    for key, value in input_dict.items():
        split_keys = [k.strip() for k in key.split(',')]
        for split_key in split_keys:
            careful_merge(split_dict, split_key, value)
    return split_dict

def get_type_dict(clust_list):
    type_dict = {}
    for pkg_dict in clust_list:
        pkgtype = pkg_dict.get('type')
        if pkgtype == 'rpm_list':
            type_dict[RPM_LIST_BASE] = type_dict.get(RPM_LIST_BASE, []) + pkg_dict.get('package_list')
        else: #image and rpm
            type_dict[pkgtype] = type_dict.get(pkgtype, []) + [pkg_dict.get('package')]
        reboot_val = pkg_dict.get(REBOOT_KEY, False)
        type_dict[REBOOT_KEY] = type_dict.get(REBOOT_KEY, False) or reboot_val
    return type_dict

def modify_addl_software(addl_dict):
    new_dict = {}
    for key, value in addl_dict.items():
        clust_list = value.get('cluster', [])
        type_dict = get_type_dict(clust_list)
        new_dict[key] = type_dict
        # import pdb; pdb.set_trace()
    return new_dict

# Example usage:
addl_soft = '/opt/omnia/input/project_default/config/rhel/9.4/additional_software.json'
roles_config = '/opt/omnia/input/project_default/roles_config.yml'

addl_soft_json_data = read_json_file(addl_soft)
roles_dict = read_roles_config(roles_config)

print("additional_software Data:")
pprint(addl_soft_json_data)
print(" ")
print("###### ROLES Data:")
pprint(roles_dict)
print("")

print("****** ADDL soft")
addl_software_dict = modify_addl_software(addl_soft_json_data)
pprint(addl_software_dict)
print("")

print("Roles + groups split DATA")
split_comma_dict = split_comma_keys(addl_software_dict)
pprint(split_comma_dict)
print("")

# intersection of split_comma_dict and roles_yaml_data
common_roles = split_comma_dict.keys() & roles_dict.keys()

for xrole in common_roles:
    print(xrole)
    # pop out the role
    bundle = split_comma_dict.pop(xrole)
    # pprint(bundle)
    # get groups from their role
    xgroup_list = roles_dict.get(xrole)

    pprint(xgroup_list)
    for xgroup in xgroup_list:
        careful_merge(split_comma_dict, xgroup, bundle)

to_all = split_comma_dict.pop('additional_software', {})
for key in split_comma_dict.keys():
    careful_merge(split_comma_dict, key, to_all)
# split_comma_dict['additional_software'] = to_all

print("  ")
print("ALLLLLLL Roles + groups split DATA")
pprint(split_comma_dict)