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

Where:

- data plugins - load data from various format and transform it in a list of dictionaries
- processor plugins - optional step, but can be used to process data before rendering
- template loaders - retrieve template content from various sources (files, directories etc.)
- renderes - iterate over list of dictionaries data and render each item with template
- returners - return rendering results to various destinations, e.g. save to file system

In addition, TTR comes with a collection of Jinja2 templates to help with common use cases,
such as generating configuration for network devices interfaces or BGP peers.

How it works
============

On the base level TTR takes list of dictionaries, renders each dictionary with template
defined in ``template_name_key`` and saves rendered data in results dictionary keyed by
``result_name_key``. Because of that each dictionary item must contain ``template_name_key``
and ``result_name_key`` keys.

Various plugins can be used to load data in a list of dictionaries with other plugins
helping to process and validate it, render and save results.

TTR API reference
=================

.. autoclass:: ttr.ttr
  :noindex:
  :members:
"""
import logging
import os
from .plugins.data import data_plugins
from .plugins.renderers import renderers_plugins
from .plugins.returners import returners_plugins
from .plugins.processors import processors_plugins
from .plugins.templates import templates_loaders_plugins
from .plugins.validate import validate_plugins
from .plugins.models import models_loaders_plugins

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
    :param templates: (str) OS pat to directory or excel spreadsheet file with templates,
        defaults to ``./Templates/`` folder
    :param template_name_key: (str) name of the key in data items that reference template
        to use to render that particular datum, default ``template``
    :param returner: (str) name of returner plugin to use, default ``self``
    :param returner_kwargs: (dict) arguments to pass on to returner plugin
    :param result_name_key: (str) name of the key in data items value of which should be
        used as a key in results dictionary, default ``device``
    :param processors: (list) list of processor plugins names to pass loaded data
        through, default is empty list - no processors applied
    :param templates_dict: (dict) dictionary of {template_name: template_content}
    :param models_dir: (str) OS path to directory or with data models, defaults to ``./Models/`` folder
    :param model_name_key: (str) name of the key in data items that reference model
        to use to validate that particular datum, default ``model``
    :param models_dict: (dict) dictionary of {model_name: model_content}
    :param validator: (str) validator plugin to use to validate provided data against models,
        default is ``yangson``
    :param validator_kwargs: (dict) arguments to pass on to validator plugin
    """

    def __init__(
        self,
        data=None,
        data_plugin=None,
        data_plugin_kwargs=None,
        renderer="jinja2",
        validator="yangson",
        renderer_kwargs=None,
        templates="./Templates/",
        models_dir="./Models/",
        template_name_key="template",
        model_name_key="model",
        returner="self",
        returner_kwargs=None,
        result_name_key="device",
        processors=None,
        processors_kwargs=None,
        templates_dict=None,
        models_dict=None,
        validator_kwargs=None,
    ):
        self.data_plugin = data_plugin
        self.data_plugin_kwargs = data_plugin_kwargs or {}
        self.templates = templates
        self.templates_dict = templates_dict or {}
        self.models_dict = models_dict or {}
        self.template_name_key = template_name_key
        self.model_name_key = model_name_key
        self.renderer = renderer
        self.validator = validator
        self.renderer_kwargs = renderer_kwargs or {}
        self.returner = returner
        self.returner_kwargs = returner_kwargs or {}
        self.result_name_key = result_name_key
        self.results = None
        self.processors = processors or {}
        self.processors_kwargs = processors_kwargs or {}
        self.data_loaded = []
        self.validator_kwargs = validator_kwargs or {}
        self.models_dir = models_dir

        # load and validate data to render
        if data:
            self.load_data(data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self.data_loaded, self.templates_dict, self.results

    def load_data(self, data, data_plugin=None):
        """
        Method to load data to render.

        :param data: (str) data to load, either OS path to data file or text
        :param data_plugin: (str) name of data plugin to load data, by default will
            choose data loader plugin based on file extension e.g. ``xlsx, csv, yaml/yml``
        """
        # decide on data loader plugin to use
        if data_plugin:
            plugin_name = data_plugin
        elif self.data_plugin:
            plugin_name = self.data_plugin
        elif os.path.isfile(data[:5000]):
            # get data loader name based on data file extension
            plugin_name = data.split(".")[-1].strip()
        else:
            raise RuntimeError(
                "ttr: failed to identify data loader plugin for '{}'".format(data[:100])
            )

        # load data using data loader plugin
        log.debug("Loading data using '{}' plugin".format(plugin_name))
        data_loaded = data_plugins[plugin_name](
            data,
            template_name_key=self.template_name_key,
            templates_dict=self.templates_dict,
            **self.data_plugin_kwargs,
        )

        # process loaded data
        data_loaded = self.process_data(data_loaded)

        # load data models for validation
        self.load_models()

        # validate loaded data
        self.validate_data(data_loaded)

        if log.isEnabledFor(logging.DEBUG):
            log.debug("Data loaded:\n{}".format(data_loaded))

        # add loaded data to overall data
        self.data_loaded.extend(data_loaded)

    def process_data(self, data):
        """
        Function to pass loaded data through a list of processor plugins.

        :param data: (list) list of dictionaries data to process
        :return: processed data
        """
        for processor_plugin in self.processors:
            log.debug(
                "ttr: running loaded data through processor: '{}'".format(
                    processor_plugin
                )
            )
            data = processors_plugins[processor_plugin](
                data=data,
                data_plugin=self.data_plugin,
                template_name_key=self.template_name_key,
                result_name_key=self.result_name_key,
                **self.processors_kwargs,
            )
        return data

    def validate_data(self, data):
        """
        Function to validate provided data

        :param data: (list) list of dictionaries data to validate
        :return: None

        Running validation raises or logs error on validation failure
        depending on value of ``on_fail`` argument in ``validator_kwargs``
        """
        for item in data:
            if self.model_name_key in item:
                model_name = item.pop(self.model_name_key)
                validate_plugins[self.validator](
                    data=item,
                    model_content=self.models_dict[model_name],
                    model_name=model_name,
                    **self.validator_kwargs,
                )

    def load_models(self, models_dir=None, model_plugin=None, **kwargs):
        """
        Function to load models content to models dictionary.

        :param models_dir: (str) OS path to directory with models, defaults to ``./Models/`` directory
        :param model_plugin: (str) models loader plugin to use - ``yangson`` (default)
        :param kwargs: any additional ``**kwargs`` to pass on to ``model_plugin`` call
        """
        models_dir = models_dir or self.models_dir
        model_plugin = model_plugin or self.validator

        # sanity checks
        if not os.path.exists(models_dir):
            log.debug(
                "ttr:load_models models_dir '{}' does not exist, do nothing".format(
                    models_dir
                )
            )
            return

        models_loaders_plugins[model_plugin](
            models_dict=self.models_dict, models_dir=models_dir, **kwargs
        )

    def load_templates(
        self,
        template_name="",
        template_content="",
        templates="",
        templates_plugin="",
        **kwargs,
    ):
        """
        Function to load templates content in templates dictionary.

        :param template_name: (str) name of template to load
        :param template_content: (str) template content to save in templates dictionary under ``template_name``
        :param templates: (str) OS pat to directory or file with templates, default ``./Templates/``
        :param templates_plugin: (str) templates loader plugin to use - ``base, xlsx, dir, file, ttr``
        :param kwargs: any additional ``**kwargs`` to pass on to ``templates_plugin``

        Decision logic:

        1. If ``template_content`` provided add it to templates dictionary under ``template_name`` key
        2. If valid ``templates_plugin`` name given use it to load template
        3. Use ``base`` templates loader plugin to load template content
        """
        if template_name and template_content:
            self.templates_dict[template_name] = template_content
        elif templates_plugin in templates_loaders_plugins:
            templates_loaders_plugins[templates_plugin](
                templates_dict=self.templates_dict,
                templates=templates,
                template_name=template_name,
                **kwargs,
            )
        else:
            templates_loaders_plugins["base"](
                templates_dict=self.templates_dict,
                templates=templates,
                template_name=template_name,
            )

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
            self.templates,
            self.templates_dict,
            self.result_name_key,
            **self.renderer_kwargs,
        )
        # return results
        log.debug("Returning results using '{}' returner".format(self.returner))
        returners_plugins[self.returner](self.results, **self.returner_kwargs)
        log.debug("TTR rendering run completed")
        if self.returner == "self":
            return self.results

        return None
