"""
File Returner Plugin
********************

**Plugin Name:** ``file``

This plugin responsible for saving results to text files
iterating over results dictionary keyed by ``result_name_key``.

For example, if results ``data_dict`` might look like this::

    {"rt-1": "interface Gi1/1\\n"
             " description Customer A\\n"
             " encapsulation dot1q 100\\n"
             " vrf forwarding  cust_a\\n"
             " ip address 10.0.0.1 255.255.255.0\\n"
             " exit\\n"
             "!\\n"
             "interface Gi1/2\\n"
             " description Customer C\\n"
             " encapsulation dot1q 300\\n"
             " vrf forwarding  cust_c\\n"
             " ip address 10.0.3.1 255.255.255.0\\n"
             " exit\\n"
             "!",
     "rt-2": "interface Gi1/2\\n"
             " description Customer B\\n"
             " encapsulation dot1q 200\\n"
             " vrf forwarding  cust_b\\n"
             " ip address 10.0.2.1 255.255.255.0\\n"
             " exit\\n"
             "!"}

If ``result_dir`` argument set to ``./Output/``, file returner
will iterate over ``data_dict`` using keys as filenames
populating files with values at the end ``./Output/`` directory
will contain two files named ``rt-1.txt`` and ``rt-2.txt`` with
respective content.
"""
import logging
import os

log = logging.getLogger(__name__)


def dump(
    data_dict, result_dir="./Output/", **kwargs
):  # pylint: disable=unused-argument
    """
    Function to save results in text files.

    :param data_dict: (dict) dictionary keyed by ``result_name_key`` where
                      values are strings to save in text files
    :param result_dir: (str) OS path to directory to save results in
    :param kwargs: (dict) any additional arguments ignored
    """
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for datum_name, filedata in data_dict.items():
        filename = os.path.join(result_dir, "{}.txt".format(datum_name))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(filedata)
