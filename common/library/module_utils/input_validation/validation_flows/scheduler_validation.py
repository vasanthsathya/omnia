import json
from ansible.module_utils.input_validation.common_utils import validation_utils
from ansible.module_utils.input_validation.common_utils import config
from ansible.module_utils.input_validation.common_utils import en_us_validation_msg

def validate_k8s_parameters(admin_static_range, bmc_static_range, admin_dynamic_range, bmc_dynamic_range, pod_external_ip_range, k8s_service_addresses, k8s_pod_network_cidr):
    # Check IP range overlap between omnia IPs, admin network, and bmc network
    results=[]
    ip_ranges = [admin_static_range, bmc_static_range, admin_dynamic_range, bmc_dynamic_range, pod_external_ip_range, k8s_service_addresses, k8s_pod_network_cidr]
    does_overlap, _ = validation_utils.check_overlap(ip_ranges)

    if does_overlap:
        results.append("The IP range define is not correct.")

    return results



