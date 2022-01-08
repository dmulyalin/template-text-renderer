"""
File Template Loader
********************

**Reference name** ``file``

Loads template for rendering from file.
"""

import os
import logging
import traceback

log = logging.getLogger(__name__)


def load(
    template_name, templates_dict, filepath=None, **kwargs
):  # pylint: disable=unused-argument
    """
    Function to load template content from ``file`` path.

    :param template_name: (str) name of template to load, should point to file
        if no ``filepath`` argument provided
    :param templates_dict: (str) dictionary to store template content in
    :param filepath: (str) optional, path to file to open
    :param kwargs: (dict) any additional arguments ignored
    :return: ``True`` on success and ``False`` on failure to load template
    """
    # load template content
    try:
        if filepath and os.path.isfile(filepath):
            with open(filepath, encoding="UTF-8", mode="r") as f:
                templates_dict[template_name] = f.read()
        elif os.path.isfile(template_name):
            with open(template_name, encoding="UTF-8", mode="r") as f:
                templates_dict[template_name] = f.read()
        else:
            raise RuntimeError(
                "TTR:file_template_loader filepath '{}' and template_name '{}' not pointing to file".format(
                    filepath, template_name
                )
            )
    except:
        log.error(
            "TTR:file_template_loader - failed open template: {}; error: {}".format(
                template_name, traceback.format_exc()
            )
        )
        return False

    return True
