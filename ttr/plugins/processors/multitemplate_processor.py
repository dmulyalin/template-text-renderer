"""
Multitemplate Processor
***********************

**Plugin reference name:** ``multitemplate``

Processor to extract multiple template dictionaries from each
data item based on suffix values.

Takes a list of dictionaries::

    [{'device': 'r1',
      'hostname': 'r1',
      'lo0_ip': '1.1.1.1',
      'lo0_ip_rollback': '1.1.1.11',
      'template': 'test_path/device_base',
      'template_rollback': 'test_path/device_base_rollback'},
     {'device:a': 'r1',
      'device:b': 'r2',
      'interface:a': 'Eth1',
      'interface:b': 'Eth1',
      'ip:a': '10.0.0.1',
      'ip:b': '10.0.0.2',
      'mask': 24,
      'template:a': 'test_path/interf_cfg',
      'template:b': 'test_path/interf_cfg_b'}]

Returns::

    [{'device': 'r1',
    'hostname': 'r1',
    'lo0_ip': '1.1.1.11',
    'template': 'test_path/device_base_rollback'},
    {'device': 'r1',
    'hostname': 'r1',
    'lo0_ip': '1.1.1.1',
    'template': 'test_path/device_base'},
    {'device': 'r1',
    'interface': 'Eth1',
    'ip': '10.0.0.1',
    'mask': 24,
    'template': 'test_path/interf_cfg'},
    {'device': 'r2',
    'interface': 'Eth1',
    'ip': '10.0.0.2',
    'mask': 24,
    'template': 'test_path/interf_cfg_b'}]

Where ``template_name_key`` is ``template``.

Multitemplate processor detects suffixes/endings, ``:a`` and ``:b``
in this case, and uses them to split dictionaries apart,
populating them with values corresponding to certain suffixes.

Key names without suffixes considered as common values and shared across
all dictionaries.
"""
import logging

log = logging.getLogger(__name__)


def process(data, template_name_key, **kwargs):  # pylint: disable=unused-argument
    """
    Function to process multitemplate data items.

    :param data: (list), data to process - list of dictionaries
    :param template_name_key: string, name of the template key
    :param kwargs: (dict) any additional arguments ignored
    """
    ret = []
    headers = tuple()
    previous_headers = tuple()
    headers_to_endings = {}

    # scan through data to split in multiple items
    for datum in data:

        headers = tuple(datum.keys())

        # check if need to form headers_to_endings dictionary of {ending: [headers]}
        if headers != previous_headers:
            endings = tuple(
                [
                    h.replace(template_name_key, "")
                    for h in headers
                    if (
                        isinstance(h, str)
                        and h.startswith(template_name_key)
                        and h != template_name_key
                    )
                ]
            )
            headers_without_endings = [
                h for h in headers if (isinstance(h, str) and not h.endswith(endings))
            ]
            headers_to_endings = {
                ending: headers_without_endings
                + [h for h in headers if (isinstance(h, str) and h.endswith(ending))]
                for ending in endings
            }
            if template_name_key in headers_without_endings:
                headers_to_endings = {"": headers_without_endings, **headers_to_endings}
        # form data
        for ending, headers_item in headers_to_endings.items():
            ret.append(
                {
                    h[: -len(ending)] if h.endswith(ending) and ending else h: datum[h]
                    for h in headers_item
                }
            )
        previous_headers = headers
    return ret
