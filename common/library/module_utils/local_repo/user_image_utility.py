import requests
from requests.auth import HTTPBasicAuth
from ansible.module_utils.local_repo.config import (
    pulp_container_commands
)

def check_image_in_registry(host, image, tag, cacert, key, username, password, logger):
    """
    Check if a container image exists in a user registry using Docker Registry HTTP API v2.

    Args:
        host (str): Registry hostname.
        image (str): Image name (e.g., library/nginx).
        tag (str): Image tag (e.g., 1.25.2-alpine).
        cacert (str): Path to the CA certificate file.
        key (str): Path to the client key file.
        username (str): Registry username.
        password (str): Registry password.
        logger (logging.Logger): Logger instance.

    Returns:
        bool: True if image exists, False otherwise.
    """
    image_url = f"https://{host}/v2/{image}/manifests/{tag}"
    logger.info(f"Checking image existence at: {image_url}")

    try:
        response = requests.get(
            image_url,
            auth=HTTPBasicAuth(username, password),
            cert=(cacert, key),
            verify=cacert,
            timeout=10
        )

        if response.status_code == 200:
            logger.info(f"Image '{image}:{tag}' exists in registry '{host}'")
            return True
        else:
            logger.warning(f"Image not found (HTTP {response.status_code}) in registry '{host}'")
            return False


def process_user_registry(package, host, package_content, version_variables, logger):
    """
    Sets up and syncs a user container image repository using a tag or digest.

    Args:
        package (dict): Package metadata with 'package', and either 'tag' or 'digest'.
        host (str): Registry host URL.
        package_content (str): Image name to process.
        version_variables (dict): Variables to render the tag if templated.
        logger (Logger): Logger for debug and error output.

    Returns:
        tuple: (bool success, str image_identifier)
    """
    logger.info("#" * 30 + f" {process_user_registry.__name__} start " + "#" * 30)

    user_reg_prefix = "user_reg_"
    repository_name = f"{user_reg_prefix}{package['package'].replace('/', '_').replace(':', '_')}"
    remote_name = f"remote_{package['package'].replace('/', '_')}"
    package_identifier = package['package']
    policy_type = "immediate"
    base_url = f"https://{host}/"

    logger.info("Creating user container repository")
    with repository_creation_lock:
        result = create_container_repository(repository_name, logger)
    if result is False or (isinstance(result, dict) and result.get("returncode", 1) != 0):
        return False, package_identifier

    logger.info("Creating user registry remote")
    if "digest" in package:
        package_identifier += f":{package['digest']}"
        result = create_user_remote_digest(remote_name, base_url, package_content, policy_type, logger)
        if result is False or (isinstance(result, dict) and result.get("returncode", 1) != 0):
            return False, package_identifier

    elif "tag" in package:
        tag_template = Template(package.get('tag', None))
        tag_val = tag_template.render(**version_variables)
        package_identifier += f":{package['tag']}"
        with remote_creation_lock:
            result = create_user_remote_tag(remote_name, base_url, package_content, policy_type, tag_val, logger)
        if result is False or (isinstance(result, dict) and result.get("returncode", 1) != 0):
            return False, package_identifier

    logger.info("Syncing remote for user container repository")
    result = sync_container_repository(repository_name, remote_name, package_content, logger)
    if result is False or (isinstance(result, dict) and result.get("returncode", 1) != 0):
        return False, package_identifier

    logger.info("#" * 30 + f" {process_user_registry.__name__} end " + "#" * 30)
    return True, package_identifier

def handle_user_image_registry(package, package_content, version_variables, user_registries, logger):
    """
    Checks user-defined container registries for the presence of a 
    specific image (by tag or digest) and processes it if found.

    Parameters:
        package (dict): Dictionary containing package metadata.
        package_content (str): Image name or content identifier.
        version_variables (dict): Variables used to render the tag template.
        user_registries (list): List of user registries with required authentication and TLS information.
        logger (logging.Logger): Logger object for logging messages.

    Returns:
        bool: True if image is found and successfully processed; False otherwise.
    """
    logger.info("#" * 30 + f" {handle_user_image_registry.__name__} start " + "#" * 30)
    result = False
    package_info = None
    image_name = package_content

    try:
        # Determine tag or digest for the image
        if "tag" in package:
            tag_template = Template(package["tag"])
            tag_val = tag_template.render(**version_variables)
        elif "digest" in package:
            digest_hash = package["digest"]
            tag_val = f"sha256:{digest_hash}"

        for registry in user_registries:
            host = registry.get("host")
            cacert = registry.get("cacert_path")
            key = registry.get("key_path")
            username = registry.get("username")
            password = registry.get("password")

            if not all([host, cacert, key, username, password]):
                logger.warning(f"Skipping registry with missing fields: {registry}")
                continue

            logger.info(f"Checking image {image_name}:{tag_val} in registry {host}")
            image_found = check_image_in_registry(
                host=host,
                image=image_name,
                tag=tag_val,
                cacert=cacert,
                key=key,
                username=username,
                password=password,
                logger=logger
            )

            if image_found:
                logger.info(f"Image '{image_name}:{tag_val}' found in registry '{host}'")
                result, package_info = process_user_registry(package, host, package_content, version_variables, logger)
                break

    except Exception as e:
        logger.error(f"Exception in {handle_user_image_registry.__name__}: {e}")
        result = False

    logger.info("#" * 30 + f" {handle_user_image_registry.__name__} end " + "#" * 30)
    return result
