"""
Self Returner Plugin
********************

**Plugin Name:** ``self``

This plugin does nothing with results, implementing
behaviour where results stored in TTR object for 
further programmatic consumption.
"""

def dump(data_dict, **kwargs):
    """
    This function applying no actions to results,
    and implemented to keep plugins API consistent.
    
    :param data_dict: (dict) dictionary keyed by ``result_name_key`` where 
                      values are rendered results string
    """
    pass