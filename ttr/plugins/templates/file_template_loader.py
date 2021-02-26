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


def load(template_name, templates_dict, filepath=None, **kwargs):
    """
    Function to load template content from ``file`` path.
    
    :param template_name: (str) name of template to load, should point to file 
        if no ``filepath`` argument provided
    :param templates_dict: (str) dictionary to store template content in
    :param filepath: (str) optional, path to file to open
    :return: ``True`` on success and ``False`` on failure to load template    
    """       
    # load template content
    try:
        if filepath:
            with open(filepath, "r") as f:
                templates_dict[template_name] = f.read()             
        else:
            with open(template_name, "r") as f:
                templates_dict[template_name] = f.read()  
    except:
        tb = traceback.format_exc()
        log.error("TTR:file_template_loader - failed open template: {}; error: {}".format(template_name, tb))
        return False
        
    return True