"""
Templates Split Processor
*************************

**Plugin reference name:** ``templates_split``

Processor to support definition of several templates separated by 
delimiter (default - ``;``) consequentially splitting data into 
several items with dedicated template.

Takes a list of dictionaries, for example::

    [{'device': 'r1',
      'hostname': 'r1',
      'lo0_ip': '1.1.1.1',
      'lo0_ip_rollback': '1.1.1.11',
      'template': 'device_base; isis_base; bgp_base'},
     {'device': 'r2',
      'hostname': 'r2',
      'lo0_ip': '1.1.1.2',
      'lo0_ip_rollback': '1.1.1.22',
      'template': 'device_base; bgp_base'}]

After splitting templates ``templates_split`` processor returns::

    [{'device': 'r1',
      'hostname': 'r1',
      'lo0_ip': '1.1.1.1',
      'lo0_ip_rollback': '1.1.1.11',
      'template': 'device_base'},
     {'device': 'r1',
      'hostname': 'r1',
      'lo0_ip': '1.1.1.1',
      'lo0_ip_rollback': '1.1.1.11',
      'template': 'isis_base'},
     {'device': 'r1',
      'hostname': 'r1',
      'lo0_ip': '1.1.1.1',
      'lo0_ip_rollback': '1.1.1.11',
      'template': 'bgp_base'},      
     {'device': 'r2',
      'hostname': 'r2',
      'lo0_ip': '1.1.1.2',
      'lo0_ip_rollback': '1.1.1.22',
      'template': 'device_base'},
     {'device': 'r2',
      'hostname': 'r2',
      'lo0_ip': '1.1.1.2',
      'lo0_ip_rollback': '1.1.1.22',
      'template': 'bgp_base'}]
"""

import logging

log = logging.getLogger(__name__)

def process(data, template_name_key, split_char=";", **kwargs):
    """
    Function to split templates. e.g. if ``template_name_key`` value
    contains several templates, this processor will split them using
    ``split_char`` and produce data item for each template coping data 
    accordingly.
    
    :param data: list of dictionaries to process
    :param template_name_key: string, name of the template key
    :param split_char: str, character to use to split template names
    """
    ret = []
    
    # iterate over data and split templates
    while data:
        item = data.pop(0)
        # run sanity check
        if not isinstance(item.get(template_name_key, None), str):
            continue
        # do templates split if any
        if split_char in item[template_name_key]:
            templates = [i.strip() for i in item.pop(template_name_key).split(split_char)]
            for t_name in templates:
                item_copy = item.copy()
                item_copy[template_name_key] = t_name
                ret.append(item_copy)
        else:
            ret.append(item)
            
    del data
    return ret