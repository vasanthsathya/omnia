import json
import yaml
import os
from ansible.module_utils.basic import AnsibleModule

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
    all_groups = list(data.get('Groups', {}).keys())
    return role_cfg, all_groups

def careful_merge(split_dict, split_key, value):
    val_d = split_dict.get(split_key, {})
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
    return new_dict

def main():
    module = AnsibleModule(
        argument_spec={
            'software_bundle': {'type': 'path'},
            'roles_config': {'type': 'path'},
            'software_config': {'type': 'path'},
            'input_path': {'type': 'path'},
            'software_bundle_key': {'type': 'str', 'default': 'additional_software'}
        },
        mutually_exclusive=[
            ('input_path', 'software_config'),
            ('input_path', 'roles_config'),
            ('input_path', 'software_bundle')
        ],
        required_one_of=[
            ('input_path', 'software_config', 'roles_config', 'software_bundle')
        ],
        required_together=[
            ('software_config', 'roles_config', 'software_bundle')
        ],
        supports_check_mode=True
    )
    
    inp_path = module.params.get('input_path')
    addl_key = module.params['software_bundle_key']
    if inp_path:
        inp_path = inp_path.rstrip('/')
        #TODO: check if inp_path exists and is directory else ,module.fail_json
        sw_cfg_path = inp_path + '/software_config.json'
        sw_cfg_data = read_json_file(sw_cfg_path)
        addl_soft = f"{inp_path}/config/{sw_cfg_data['cluster_os_type']}/{sw_cfg_data['cluster_os_version']}/{addl_key}.json"
        roles_config = f"{inp_path}/roles_config.yml"
    else:
        addl_soft = module.params.get('software_bundle')
        roles_config = module.params.get('roles_config')
        sw_cfg_data =  read_json_file(module.params.get('software_config'))

    sw_list = [sw_dict.get('name') for sw_dict in sw_cfg_data.get('softwares')]
    if addl_key not in sw_list:
        module.exit_json(msg=f"{addl_key} not found in {sw_list}", grp_pkg_map={})
    req_addl_soft_list = [sub_group.get('name') for sub_group in sw_cfg_data.get(addl_key, [])]
    req_addl_soft_list.append(addl_key) # add the additional_software key

    addl_soft_json_data = read_json_file(addl_soft)
    req_addl_soft = {sub_group: addl_soft_json_data.get(sub_group) for sub_group in req_addl_soft_list}

    roles_dict, all_groups = read_roles_config(roles_config)
    temp_addl_pkgs = req_addl_soft.pop(addl_key, {})
    req_addl_soft[','.join(all_groups)] = temp_addl_pkgs
    addl_software_dict = modify_addl_software(req_addl_soft)
    split_comma_dict = split_comma_keys(addl_software_dict)

    # intersection of split_comma_dict and roles_yaml_data
    common_roles = split_comma_dict.keys() & roles_dict.keys()

    for xrole in common_roles:
        bundle = split_comma_dict.pop(xrole)
        xgroup_list = roles_dict.get(xrole)
        for xgroup in xgroup_list:
            careful_merge(split_comma_dict, xgroup, bundle)

    changed = True
    module.exit_json(changed=changed, grp_pkg_map=split_comma_dict, msg="Successfully fetched and mapped groups and packages")

if __name__ == "__main__":
    main()
