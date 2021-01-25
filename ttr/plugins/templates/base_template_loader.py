"""
Base Template Loader
********************

Base loader loads templates from ``.txt`` files. 

.. warning:: Only ``.txt`` files supported by this loader.

This loader searches for templates in this order:

0. Check if template with given name already loaded, use it if so
1. Check if template name starts with ``ttr://``, load it from TTR package if so
2. If template name references file, load it
3. Use ``templates_dir`` as a directory to search for template file.

For cases 1 and 3 template name can omit extension, base loader will assume
``.txt`` extension in that case. 

On failure to load template file, base loader will log an error message and
TTR continue processing of other data items.
"""

import os
import logging

log = logging.getLogger(__name__)


def load(template_name, templates_dict, templates_dir):
    """
    Function to locate template file and return it's content
    
    **Attributes**
    
    * template_name (str) - OS path to template file relative to execution folder 
      or to /ttr/templates/ package directory or name of template within spreadsheet
    * templates_dir (str) - name of directory with templates
    * templates_dict (dict) - dictionary of templates content
    
    **Valid combinations of template location**
       
    * ``template_name="./misc/foo/bar.txt"`` 
    * ``template_name="ttr://misc/foo/bar.txt"``   
    
    On success loads template content in ``templates_dict`` and returns ``True``, on failure
    returns ``False``
    """
    # check if template already loaded
    if template_name in templates_dict:
        return True
    # check if template_name referring to template in TTR package
    elif template_name.startswith("ttr://"):
        template_filepath = template_name.replace("ttr://", "")
        if not template_filepath.endswith(".txt"):
            template_filepath = "{}.txt".format(template_filepath)
        # construct path "<abs path>\ttr\plugins\templates\..\..\templates\<template name>" 
        # to move to ttr package dir and down to templates directory
        template_filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..", "templates", template_filepath)
    # check if template_name is a path to file
    elif os.path.isfile(template_name):
        template_filepath = template_name
    # assume that template_name is a path to text file within templates_dir
    else:
        template_filepath = os.path.join(
            templates_dir, template_name if template_name.endswith(".txt") else "{}.txt".format(
                template_name
            )
        )
        
    # load template content from file
    if os.path.isfile(template_filepath):
        with open(template_filepath, "r") as f:
            templates_dict[template_name] = f.read()        
    else:
        log.error("TTR:load_template template not found: {}; formed template_filepath: {}".format(template_name, template_filepath))
        return False

    return True
