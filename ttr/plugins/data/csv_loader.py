"""
CSV Spreadsheets loader plugin
******************************

**Plugin Name:** ``csv``

Support loading data from CSV text file.

Spreadsheet must contain a column or multiple columns with headers starting
with ``template_name_key`` argument string. Values of template(s) columns either
names of the template to use for rendering or OS path string to template file
relative to ``template_dir`` argument supplied to TTR object on instantiation.

In addition, table must contain column with ``result_name_key`` values, they used
to combine results, i.e. rendering results for identical ``result_name_key`` combined
in a single string. ``result_name_key`` used further by returners to return results.
"""
import logging
import csv
import os

log = logging.getLogger(__name__)


def load(
    data, templates_dict=None, template_name_key=None, **kwargs
):  # pylint: disable=unused-argument
    """
    Function to load CSV spreadsheet.

    :param data: OS path to CSV text file
    :param templates_dict: (dict) dictionary to load templates from spreadsheet, not supported by csv loader
    :param template_name_key: (str) templates column header prefix, not supported by csv loader
    :param kwargs: (dict) any additional arguments to pass on to ``csv.DictReader``
        object instantiation
    """
    ret = None

    # load from file
    if os.path.isfile(data):
        with open(data, newline="") as csvfile:
            reader = csv.DictReader(csvfile, **kwargs)
            ret = [dict(row) for row in reader]
    # load all csv files from folder
    elif os.path.isdir(data):
        pass
    # load data text as is using stringio module
    elif isinstance(data, str):
        pass
    else:
        raise SystemExit(
            "csv_loader, unsupported data, should be either OS path to file, directory or text"
        )

    return ret
