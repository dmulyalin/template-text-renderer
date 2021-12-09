"""
TTR Template Loader
********************

**Reference name** ``ttr``

Loads templates for rendering from TTR package.
"""

import os
import logging
import traceback

log = logging.getLogger(__name__)


def load(template_name, templates_dict, **kwargs):  # pylint: disable=unused-argument
    """
    Function to load template content from ``ttr://...`` path.

    :param template_name: (str) name of template to load
    :param templates_dict: (str) dictionary to store template content in
    :param kwargs: (dict) any additional arguments ignored
    :return: ``True`` on success and ``False`` on failure to load template
    """
    # construct path "<abs path>\ttr\plugins\templates\..\..\templates\<template name>"
    # to move to ttr package dir and down to templates directory
    template_filepath = template_name.replace("ttr://", "")
    template_filepath = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "..",
        "..",
        "templates",
        template_filepath,
    )

    # check if template_filepath is path to file and try adding .txt extension to if not
    if not os.path.isfile(template_filepath) and not template_filepath.endswith(".txt"):
        template_filepath = "{}.txt".format(template_filepath)

    # load template content
    try:
        with open(template_filepath, "r") as f:
            templates_dict[template_name] = f.read()
    except:
        log.error(
            "TTR:ttr_template_loader - failed open template: {}; template_filepath: {}; error: {}".format(
                template_name, template_filepath, traceback.format_exc()
            )
        )
        return False

    return True
