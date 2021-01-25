"""
Template Text Renderer - TTR
############################

Module to produce text files using templates. TTR targets to implement common work flow:

.. image:: ./_images/workflow.png

Above approach is fairly simple but powerful enough to address various use cases
where structured data need to be transformed in a textual form understandable by
targeted system.

TTR uses plugins to load data and templates, render and return results.

.. image:: ./_images/Plugins_overview.png

In addition, TTR comes with a collection of Jinja2 templates to help with
common use cases.
"""
__version__ = "0.1.0"

import logging
import os
from .plugins.data import data_plugins
from .plugins.renderers import renderers_plugins
from .plugins.returners import returners_plugins
from .plugins.processors import processors_plugins

log = logging.getLogger(__name__)


class ttr:
    """
    Main class to instantiate TTR object.

    :param data: (str) type depends on data plugin in use, but can be an OS
        path string referring to YAML structured text file or CSV spreadsheet
    :param data_plugin: (str) name of data plugin to use to load data
    :param data_plugin_kwargs: (dict) arguments to pass on to data plugin
    :param renderer: (str) name of renderer plugin to use, default ``jinja2``
    :param renderer_kwargs: (dict) arguments to pass on to renderer plugin
    :param templates_dir: (str) OS pat to directory with templates, default ``./Templates/``
    :param template_name_key: (str) name of the key in data items that reference template
        to use to render that particular datum, default ``template``
    :param returner: (str) name of returner plugin to use, default ``self``
    :param returner_kwargs: (dict) arguments to pass on to returner plugin
    :param result_name_key: (str) name of the key in data items value of which should be
        used as a key in results dictionary, default ``device``
    :param processors: (list) list of processor plugins names to pass loaded data
        through, default is empty list - no processors applied
    :param templates_dict: (dict) dictionary of {template_name: template_content}
    """
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
        processors=[],
        templates_dict={}
    ):
        self.data_plugin = data_plugin
        self.data_plugin_kwargs = data_plugin_kwargs
        self.templates_dir = templates_dir
        self.templates_dict = templates_dict or {}
        self.template_name_key = template_name_key
        self.renderer = renderer
        self.renderer_kwargs = renderer_kwargs
        self.returner = returner
        self.returner_kwargs = returner_kwargs
        self.result_name_key = result_name_key
        self.results = None
        self.processors = processors
        self.data_loaded = None

        # load data to render
        if data:
            self.load_data(data)


    def __enter__(self):
        return self


    def __exit__(self, type, value, traceback):
        del self.data_loaded, self.templates_dict, self.results


    def load_data(self, data, data_plugin=None):
        """
        Method to load data to render.

        :param data: (str) data to load, either OS path to data file or text
        :param data_plugin: (str) name of data plugin to load data, by default
            will choose data plugin based on file extension
        """
        if data_plugin:
            plugin_name = data_plugin
        elif self.data_plugin:
            plugin_name = self.data_plugin
        elif os.path.isfile(data[:5000]):
            # get data loader name based on data file extension
            plugin_name = data.split(".")[-1].strip()
        else:
            log.error("load_data: failed to identify data plugin to load data '{}'".format(data[:100]))
            return

        # load data using plugin
        log.debug("Loading data using '{}' plugin".format(plugin_name))
        self.data_plugin_kwargs.setdefault("template_name_key", self.template_name_key)
        self.data_plugin_kwargs["templates_dict"] = self.templates_dict
        self.data_loaded = data_plugins[plugin_name](data, **self.data_plugin_kwargs)

        # process loaded data
        for processor_plugin in self.processors:
            log.debug("Running loaded data through processor: '{}'".format(processor_plugin))
            self.data_loaded = processors_plugins[processor_plugin](
                self.data_loaded,
                data_plugin=self.data_plugin,
                template_name_key=self.template_name_key
            )

        log.debug("Data '{}' loaded".format(str(data)[:40]))

    def run(self):
        """
        Method to render templates with data and produce dictionary results
        keyed by ``result_name_key``.

        If returner set to ``self``, will return results dictionary.
        """
        # generate results
        log.debug("Rendering data using '{}' renderer".format(self.renderer))
        self.results = renderers_plugins[self.renderer](
            self.data_loaded,
            self.template_name_key,
            self.templates_dir,
            self.templates_dict,
            self.result_name_key,
            **self.renderer_kwargs
        )
        # return results
        log.debug("Returning results using '{}' returner".format(self.returner))
        returners_plugins[self.returner](
            self.results,
            **self.returner_kwargs
        )
        log.debug("TTR rendering run completed")
        if self.returner == "self":
            return self.results
