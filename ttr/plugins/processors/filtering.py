"""
Filtering Processor
*******************

**Plugin reference name:** ``filtering``

Processor to filter data using glob patterns. Filtering done
against ``result_name_key`` values.

Takes a list of dictionaries, for example::

    [{'device': 'rr21',
      'lo0_ip': '1.1.1.1',
      'lo0_ip_rollback': '1.1.1.11',
      'template': 'device_base},
     {'device': 'core-1',
      'lo0_ip': '1.1.1.2',
      'lo0_ip_rollback': '1.1.1.22',
      'template': 'device_base}]

If filter pattern is ``core-*`` and ``result_name_key`` is ``device``, 
``filtering`` processor will return::

    [{'device': 'core-1',
      'lo0_ip': '1.1.1.2',
      'lo0_ip_rollback': '1.1.1.22',
      'template': 'device_base}]
"""

import logging
from fnmatch import fnmatchcase

log = logging.getLogger(__name__)

def process(data, result_name_key, filters=[], **kwargs):
    """
    Function to filter data using glob patterns.
    
    :param data: list of dictionaries to process
    :param filters: list, list of glob patterns to use for filtering. Filtering successful
        if at list one pattern matches
    :param result_name_key: (str) name of the key in data items value of which should be
        used as a key in results dictionary, default ``device``. Filtering done against
        values defined under ``result_name_key``
    """
    if not any(filters):
        return data
        
    ret = []
    
    # iterate over data and filter it
    while data:
        item = data.pop(0)
        # run sanity checks
        if not isinstance(item.get(result_name_key, None), str):
            log.warning("TTR:filtering processor - result_name_key '{}' invalid value: {}".format(
                    result_name_key, item
                )
            )
            continue
        for pattern in filters:
            # run filtering
            if fnmatchcase(item[result_name_key], str(pattern)):
                ret.append(item)
                break
                
    return ret