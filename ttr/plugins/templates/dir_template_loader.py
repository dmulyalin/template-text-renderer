"""
Directory Template Loader
*************************

**Reference name** ``dir``

Loads template for rendering from file in directory
"""

import os
import logging
import traceback

log = logging.getLogger(__name__)


def load(
    template_name, templates_dict, templates, **kwargs
):  # pylint: disable=unused-argument
    """
    Function to load template content from file in directory.

    :param template_name: (str) name of template to load, should point to file
    :param templates_dict: (str) dictionary to store template content in
    :param templates: (str) OS path to directory with template file
    :param kwargs: (dict) any additional arguments ignored
    :return: ``True`` on success and ``False`` on failure to load template
    """
    # try to use template_name as is
    template_filepath = os.path.join(templates, template_name)

    # check if path referring a file, if not, append .txt to template file name
    if not os.path.isfile(template_filepath) and not template_name.endswith(".txt"):
        template_filepath = os.path.join(templates, "{}.txt".format(template_name))

    # load template content
    try:
        with open(template_filepath, "r") as file:
            templates_dict[template_name] = file.read()
    except:
        log.error(
            "TTR:dir_template_loader - failed open '{}' template from '{}' directory; formed path: '{}'; error: {}".format(
                template_name, templates, template_filepath, traceback.format_exc()
            )
        )
        return False

    return True
