"""
YAML loader
***********

**Plugin Name:** ``yaml``

**Prerequisites:**

- Requires PyYAML library

Plugin to load data to render from YAML structured text.
"""
import logging
import os

log = logging.getLogger(__name__)

try:
    from yaml import safe_load
except ImportError:
    log.error(
        "yaml_loader: failed to import YAML module, install: 'python -m pip install pyyaml'"
    )


def load(
    data, templates_dict=None, template_name_key=None, **kwargs
):  # pylint: disable=unused-argument
    """
    Function to load YAML data from text file or from string. Text file should have
    ``.yml`` or ``.yaml`` extension to properly detect loader.

    :param data: string, OS path to text file or YAML structured text
    :param templates_dict: (dict) dictionary to load templates from spreadsheet, not supported by yaml loader
    :param template_name_key: (str) templates column header prefix, not supported by yaml loader
    :param kwargs: (dict) any additional arguments are ignored
    """
    ret = None

    # load from file
    if os.path.isfile(data[:1000]):
        with open(data, newline="", encoding="UTF-8") as yamlfile:
            ret = safe_load(yamlfile)
    # load as is
    elif isinstance(data, str):
        ret = safe_load(data)
    else:
        raise SystemExit(
            "yaml_loader, unsupported data, should be either OS path to file or text"
        )

    return ret
