"""
EBORN
=====


"""
__version__ = "0.1.0"

import logging
import os
from .plugins.data import data_plugins
from .plugins.renderers import renderers_plugins
from .plugins.returners import returners_plugins
from .plugins.processors import processors_plugins

log = logging.getLogger(__name__)


class eborn:
    
    def __init__(
        self, 
        data=None, 
        data_plugin=None, 
        data_plugin_kwargs={},
        renderer="jinja2",
        renderer_kwargs={},
        templates_dir="./Templates/",
        template_name_key="template",
        returner="self",
        returner_kwargs={},
        result_name_key="device",
        processors=["multitemplate"]
    ):
        self.data_plugin = data_plugin
        self.data_plugin_kwargs = data_plugin_kwargs
        self.templates_dir = templates_dir
        self.templates_dict = {} # dictionary of {template_name: template_content}
        self.template_name_key = template_name_key
        self.renderer = renderer
        self.renderer_kwargs = renderer_kwargs
        self.returner = returner
        self.returner_kwargs = returner_kwargs
        self.result_name_key = result_name_key
        self.results = None
        self.processors = processors
        
        # load data to render
        if data:
            self.load_data(data)


    def __enter__(self):
        return self
        
        
    def __exit__(self, type, value, traceback):
        del self.data_loaded, self.templates_dict, self.results
        
    
    def load_data(self, data):
        """
        Method to load data to render
        """
        if self.data_plugin:
            plugin_name = self.data_plugin
        elif os.path.isfile(data[:5000]):
            # get data loader name based on data file extension
            plugin_name = data.split(".")[-1].strip()
            
        # load data using plugin
        self.data_plugin_kwargs.setdefault("template_name_key", self.template_name_key)
        self.data_plugin_kwargs["templates_dict"] = self.templates_dict
        self.data_loaded = data_plugins[plugin_name](data, **self.data_plugin_kwargs)
        
        # process loaded data
        for processor_plugin in self.processors:
            self.data_loaded = processors_plugins[processor_plugin](
                self.data_loaded, 
				data_plugin=self.data_plugin,
                template_name_key=self.template_name_key
            )
            
        
    def run(self):
        """
        Method to render templates with data and produce results dictionary
        """   
        # generate results
        self.results = renderers_plugins[self.renderer](
            self.data_loaded, 
            self.template_name_key,
            self.templates_dir, 
            self.templates_dict,
            self.result_name_key,
            **self.renderer_kwargs
        )
        # return results
        returners_plugins[self.returner](
            self.results, 
            **self.returner_kwargs
        )
        if self.returner == "self":
            return self.results