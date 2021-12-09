from . import base_template_loader
from . import xlsx_template_loader
from . import ttr_template_loader
from . import file_template_loader
from . import dir_template_loader

templates_loaders_plugins = {
    "base": base_template_loader.load,
    "xlsx": xlsx_template_loader.load,
    "ttr": ttr_template_loader.load,
    "file": file_template_loader.load,
    "dir": dir_template_loader,
}
