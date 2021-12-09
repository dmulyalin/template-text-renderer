"""
Self Returner Plugin
********************

**Plugin Name:** ``self``

This plugin does nothing with results, implementing
behavior where results stored in TTR object for
further programmatic consumption.
"""


def dump(data_dict, **kwargs):  # pylint: disable=unused-argument
    """
    This function applying no actions to results,
    implemented to keep plugins API consistent.

    :param data_dict: (dict) dictionary keyed by ``result_name_key`` where
        values are rendered results string
    :param kwargs: (dict) any additional arguments ignored
    """
    # do nothing
