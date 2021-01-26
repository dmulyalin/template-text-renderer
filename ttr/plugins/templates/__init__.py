from . import base_template_loader
from . import xlsx_template_loader

templates_loaders_plugins = {
    "base": base_template_loader.load,
    "xlsx": xlsx_template_loader.load
}