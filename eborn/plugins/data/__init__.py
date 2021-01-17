from . import csv_loader
from . import xlsx_loader

data_plugins = {
    "csv": csv_loader.load,
    "xlsx": xlsx_loader.load
}