from . import csv_loader
from . import xlsx_loader
from . import yaml_loader

data_plugins = {
    "csv": csv_loader.load,
    "xlsx": xlsx_loader.load,
    "yaml": yaml_loader.load,
    "yml": yaml_loader.load,
}
