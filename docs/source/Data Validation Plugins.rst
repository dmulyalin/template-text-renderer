Data Validation Plugins
#######################

Data validation plugins responsible for validating loaded data to make sure it adheres
to model or schema requirements.

By default TTR uses ``yangson`` plugin for data validation, alternatively TTR object 
``validator`` attribute can be used to specify plugin to use.

Validation step is optional, if no models provided, data not validated. However, if required
data models can be used to make sure that correct data provided prior to performing rendering 
step.

There are two types of validation plugins:

1. Plugins to load models
2. Plugins to validate the actual data

.. automodule:: ttr.plugins.models.yangson_model_loader
.. automodule:: ttr.plugins.validate.validate_yangson
