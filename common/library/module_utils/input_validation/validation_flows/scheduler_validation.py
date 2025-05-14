import json
from ansible.module_utils.input_validation.common_utils import validation_utils
from ansible.module_utils.input_validation.common_utils import config
from ansible.module_utils.input_validation.common_utils import en_us_validation_msg

def validate_k8s_parameters(input_file_path, data, logger, module, omnia_base_dir, module_utils_base, project_name):
    results=[]

    pod_external_ip_range = data["pod_external_ip_range"]
    k8s_service_addresses = data["k8s_service_addresses"]
    k8s_pod_network_cidr = data["k8s_pod_network_cidr"]
    k8s_pod_network_cidr = data["k8s_pod_network_cidr"]
    topology_manager_policy = data["topology_manager_policy"]
    

    return results

