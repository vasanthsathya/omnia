
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.discovery.omniadb_connection import get_data_from_db # type: ignore


def check_hierarchical_provision(groups_data):
    """Check if hierarchical provisioning is required."""

    parent = groups_data.get("parent", '')
    if parent == '':
        return False
    query_result = get_data_from_db(
        table_name='cluster.nodeinfo',
        filter_dict={'service_tag': parent, 'status': 'booted', 'role': "service_node"},
    )

    if query_result:
        data = {
            query_result[0]['node']: { 'admin_ip': query_result[0]['admin_ip'],
                                        'service_tag': query_result[0]['service_tag'] }
            }
        return data
    else:
        raise ValueError(f'''Parent node - (service tag: {parent}) \
                         is not a service node or not in booted state.
        Provision the parent nodes first.''')

def get_hierarchical_data(groups_roles_info):

    hierarchical_service_data = {}
    hierarchical_provision_status = False
    for group, group_data in groups_roles_info.items():
        service_node_data = check_hierarchical_provision(group_data)
        hierarchical_provision_status = hierarchical_provision_status or bool(service_node_data)

        if not service_node_data:
            continue
        snode_name = list(service_node_data.keys())[0]
        parent_data = hierarchical_service_data.get(snode_name, {})
        parent_data.setdefault('admin_ip', service_node_data[snode_name]['admin_ip'])
        parent_data.setdefault('service_tag', service_node_data[snode_name]['service_tag'])
        parent_data.setdefault('child_groups', []).append(group)
        hierarchical_service_data[snode_name] = parent_data
        groups_roles_info[group]['hierarchical_provision_status'] = hierarchical_provision_status

    return groups_roles_info, hierarchical_service_data, hierarchical_provision_status

def main():
    module_args = dict(
        groups_roles_info=dict(type="dict", required=True)
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        groups_roles_info = module.params["groups_roles_info"]

        groups_roles_info, hierarchical_service_data, hierarchical_provision_status  = get_hierarchical_data(groups_roles_info)
        module.exit_json(
            changed=False,
            hierarchical_provision_status = hierarchical_provision_status,
            hierarchical_service_node_data = hierarchical_service_data,
            groups_roles_info = groups_roles_info
        )
    except ValueError as e:
        module.fail_json(msg=str(e))

if __name__ == "__main__":
    main()