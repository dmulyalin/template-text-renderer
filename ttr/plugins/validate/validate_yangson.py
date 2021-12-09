"""
Yangson data validation
***********************

**Reference name** ``yangson``

This plugin relies on Yangson library for data instance validation using YANG models.

.. autofunction:: ttr.plugins.validate.validate_yangson.validate
"""
import logging

log = logging.getLogger(__name__)

try:
    from yangson import enumerations

    HAS_LIBS = True
except ImportError:
    log.debug(
        "ttr.yangson_model_validator: failed to import Yangson library, make sure it is installed"
    )
    HAS_LIBS = False


def validate(
    data,
    model_content,
    model_name,
    validation_scope="all",
    content_type="all",
    on_fail="raise",
):
    """
    Validate data for compliance with YANG modules.

    :param data: (dict) dictionary data to validate
    :param model_content: (obj) Fully instantiated Yangson DataModel object
    :param model_name: (str) name of the model
    :param content_type: (str) optional, content type as per
        https://yangson.labs.nic.cz/enumerations.html supported - all, config, nonconfig
    :param validation_scope: (str) optional, validation scope as per
        https://yangson.labs.nic.cz/enumerations.html supported - all, semantics, syntax
    :param on_fail: (str) action to do if validation fails - ``raise`` (default) or ``log``

    Returns:

    * True if validation succeeded
    * False if validation failed and ``on_fail`` is "log"
    * Raises ``RuntimeError`` exception if validation failed and ``on_fail`` is "raise"
    """
    # decide on validation scopes and content
    if validation_scope == "all":
        scope = enumerations.ValidationScope.all
    elif validation_scope == "semantics":
        scope = enumerations.ValidationScope.semantics
    elif validation_scope == "syntax":
        scope = enumerations.ValidationScope.syntax
    if content_type == "all":
        ctype = enumerations.ContentType.all
    elif content_type == "config":
        ctype = enumerations.ContentType.config
    elif content_type == "nonconfig":
        ctype = enumerations.ContentType.nonconfig

    # run validation of data
    try:
        _data = {
            "{}:{}".format(model_name, k)
            if not k.startswith("{}:".format(model_name))
            else k: d
            for k, d in data.items()
        }
        inst = model_content.from_raw(_data)
        _ = inst.validate(scope=scope, ctype=ctype)
    except Exception as e:
        log.debug(
            "ttr:validate_yangson: validation failed, Original Data:\n'{}';\nPrepared Data:\n'{}',\nModel '{}';\nModel tree:\n'{}'".format(
                data, _data, model_content, model_content.ascii_tree()
            )
        )
        if on_fail == "raise":
            raise RuntimeError(
                "ttr:validate_yangson: validation failed - '{}'".format(e)
            )
        if on_fail == "log":
            log.error("ttr:validate_yangson: validation failed - '{}'".format(e))
            return False

    return True
