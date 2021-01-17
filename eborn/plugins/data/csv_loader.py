import logging
import csv
import os

log = logging.getLogger(__name__)

def load(data, templates_dict, template_name_key, **kwargs):
    ret = None
    
    # load from file
    if os.path.isfile(data):
        with open(data, newline='') as csvfile:
            reader = csv.DictReader(csvfile, **kwargs)
            ret = [dict(row) for row in reader]
    # load all csv files from folder
    elif os.path.isdir(data):
        pass
    # load data text as is using stringio module
    elif isinstance(data, str):
        pass
    else:
        raise SystemExit("csv_loader, unsupported data, should be either OS path to file, directory or text")
        
    return ret