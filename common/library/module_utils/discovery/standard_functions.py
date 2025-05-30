# Copyright 2025 Dell Inc. or its subsidiaries. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# pylint: disable=import-error,no-name-in-module,line-too-long

"""Standard functions for discovery and other modules."""

import os
import yaml
from jinja2 import Template


def create_directory(path: str, mode: int) -> None:
    """Create a directory if it does not exist, with given permissions."""
    if not os.path.exists(path):
        os.makedirs(path, mode)
    else:
        os.chmod(path, mode)


def render_template(src: str, dest: str, context: dict, module: str) -> None:
    """Render a Jinja2 template from src to dest using context."""
    try:
        with open(src, 'r') as f:
            template_content = f.read()
        template = Template(template_content)
        rendered = template.render(context)

        with open(dest, 'w') as f:
            f.write(rendered)
    except Exception as e:
        raise Exception(f"Template render error ({src} → {dest}): {str(e)}")


def load_vars_file(path: str) -> dict:
    """Load YAML variables from a file and return as a dict."""
    if not path:
        return {}
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        raise Exception(f"Failed to read vars file '{path}': {str(e)}")
