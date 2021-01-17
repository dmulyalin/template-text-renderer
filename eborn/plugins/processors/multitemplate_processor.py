import logging
import pprint

log = logging.getLogger(__name__)


def process(data, **kwargs):
    """
    Processor to extract multiple template rows from data.

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

    Where template_name_key is "template"

    :param data: data loaded by loader plugin - list of dictionaries
    :param template_name_key: string, name of the template key
    """
    ret = []
    headers = tuple()
    previous_headers = tuple()
    headers_to_endings = {}
    template_name_key = kwargs["template_name_key"]

    # scan through data to split in multiple items
    for datum in data:

        headers = tuple(datum.keys())

        # check if need to form headers_to_endings dictionary of {ending: [headers]}
        if headers != previous_headers:
            endings = tuple(
                [
                    h.replace(template_name_key, "")
                    for h in headers
                    if h.startswith(template_name_key) and h != template_name_key
                ]
            )
            headers_without_endings = [h for h in headers if not h.endswith(endings)]
            headers_to_endings = {
                ending: headers_without_endings
                + [h for h in headers if h.endswith(ending)]
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
