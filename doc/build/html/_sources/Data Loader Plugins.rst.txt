Data Loader Plugins
###################

Data plugins responsible for loading data to render from various formats
such as ``YAML`` structured text or ``xlsx`` spreadsheets.

By default TTR uses file extension to choose plugin for loading data,
alternatively TTR object ``data_plugin`` attribute can be used to 
specify default plugin to use.

For instance, to load ``data.csv`` file TTR will use ``csv`` plugin, to load
``data.yaml`` file, ``yaml`` plugin will be used, etc.

Data plugins load data in a list of dictionaries, where each item rendered using 
template as per ``template_name_key`` attribute.

.. automodule:: ttr.plugins.data.xlsx_loader
.. autofunction:: ttr.plugins.data.xlsx_loader.load


.. automodule:: ttr.plugins.data.csv_loader
.. autofunction:: ttr.plugins.data.csv_loader.load


.. automodule:: ttr.plugins.data.yaml_loader
.. autofunction:: ttr.plugins.data.yaml_loader.load


