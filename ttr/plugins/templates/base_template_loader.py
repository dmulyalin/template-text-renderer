"""
Base Template Loader
********************

**Reference name** ``base``

Base loader loads templates content in ``templates_dict`` dictionary using other loader
plugins following this order:

0. Check if template with given name already exists in ``templates_dict``, use it if so
1. Check if template name starts with ``ttr://``, load it using ``ttr_template_loader``
2. If template name references file, load it using ``file_template_loader``
3. If ``templates`` is a directory load template content using ``dir_template_loader``
4. If ``templates`` referring to ``.xlsx`` file load all templates using ``xlsx_template_loader``

On failure to load template file, base loader will log an error message and
TTR will continue processing other data items.
"""
import os
import logging

from . import xlsx_template_loader
from . import ttr_template_loader
from . import file_template_loader
from . import dir_template_loader

log = logging.getLogger(__name__)


def load(
    template_name, templates_dict, templates, **kwargs
):  # pylint: disable=unused-argument
    """
    Function to locate template file and return it's content

    **Attributes**

    :param template_name: (str) - name of template to load
    :param templates: (str) - location of templates
    :param templates_dict: (dict) - dictionary of to store template content in
    :param kwargs: (dict) any additional arguments ignored
    :return: ``True`` on success and ``False`` on failure to load template

    On success loads template content in ``templates_dict`` and returns ``True``, on failure
    returns ``False``.
    """
    # check if template already loaded
    if template_name in templates_dict:
        return True
    if not template_name:
        log.warning(
            "TTR:base_template_loader - invalid template_name '{}' value".format(
                template_name
            )
        )
        return False
    # check if template_name referring to template in TTR package
    if template_name.startswith("ttr://"):
        return ttr_template_loader.load(template_name, templates_dict)
    # check if template_name is a path to file
    if os.path.isfile(template_name):
        return file_template_loader.load(template_name, templates_dict)
    # check if templates is a path to directory then search for template_name in it
    if os.path.isdir(templates):
        return dir_template_loader.load(template_name, templates_dict, templates)
    # check if templates reference to xlsx file
    if os.path.isfile(templates) and templates.endswith(".xlsx"):
        is_loaded = xlsx_template_loader.load(
            templates_dict=templates_dict, templates=templates
        )
        log.debug(
            "TTR:base_template_loader, loaded templates from '{}', result {}".format(
                templates, is_loaded
            )
        )
        # check if template with requested name actually loaded
        return template_name in templates_dict
    # check if templates reference to txt file
    if os.path.isfile(templates) and templates.endswith(".txt"):
        return file_template_loader.load(
            template_name, templates_dict, filepath=templates
        )

    log.error(
        "TTR:base_template_loader - failed to load template: {}; templates parameter should be path to folder or xlsx spreadsheet with templates".format(
            template_name
        )
    )
    return False
