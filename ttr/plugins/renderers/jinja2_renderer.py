"""
Jinja2 Renderer Plugin
**********************

**Prerequisites:** 

- Requires `jinja2 <https://pypi.org/project/Jinja2/>`_ library

This renderer uses Jinja2 templates to render data and produce
text results.

For example, if this is a data to render expressed in YAML format::

    - interface: Gi1/1
      description: Customer A
      dot1q: 100
      ip: 10.0.0.1
      mask: 255.255.255.0
      vrf: cust_a
      template: ttr://interfaces.cisco_ios
      device: rt-1
    - interface: Gi1/2
      description: Customer B
      dot1q: 200
      ip: 10.0.2.1
      mask: 255.255.255.0
      vrf: cust_b
      template: ttr://interfaces.cisco_ios
      device: rt-2
      
``template_name_key`` corresponds to ``template`` key in above data, 
``result_name_key`` corresponds to ``device`` key in above data.

And this is the content of ``ttr://interfaces.cisco_ios`` template::

    interface {{ interface }}
     description {{ description }}
     encapsulation dot1q {{ vid }}
     vrf forwarding  {{ vrf }}
     ip address {{ ip }} {{ mask }}
     ipv6 address {{ ipv6 }}/{{ maskv6 }}
    !
    
This renderer will combine each item in above data with 
``ttr://interfaces.cisco_ios`` template and return results for further 
processing.
"""
import logging
import jinja2
import os
from ..templates import templates_loaders_plugins

log = logging.getLogger(__name__)


def render(
        data, 
        template_name_key,
        templates_dir, 
        templates_dict, 
        result_name_key,
        **renderer_kwargs
    ):
    """
    Render function takes data, templates and produces text output.
    
    :param data: (list), list of dictionaries render
    :param templates_dict: (dict), dictionary keyed by template name with template content as a value
    :param template_name_key: (str), name of template key to use for data rendering, default - ``template``
    :param result_name_key: (str), name of result key to use to combine rendering results, default - ``device``
    :param renderer_kwargs: (dict), kwargs to pass on to ``jinja2.Template(.., **kwargs)`` object instantiation
        
    By default ``renderer_kwargs`` will include::
    
        {"trim_blocks": True, "lstrip_blocks": True}
    """
    result = {}
    templates_objects_dict = {}
    
    renderer_kwargs.setdefault("trim_blocks", True)
    renderer_kwargs.setdefault("lstrip_blocks", True)
    
    # iterate over data and render it
    for datum in data:
        result_name = datum[result_name_key]
        result.setdefault(result_name, [])
        template_name = datum[template_name_key]
        
        # get template content
        if templates_loaders_plugins["base"](template_name, templates_dict, templates_dir):
            template_content = templates_dict[template_name]
        else:
            log.error(
                "TTR:Jinja2 renderer failed to load template file: '{}'".format(
                    template_name
                )
            )    
            continue

        # create Jinja2 template object
        if template_name not in templates_objects_dict:
            try:
                templates_objects_dict[template_name] = jinja2.Template(
                    template_content,
                    **renderer_kwargs
                )
            except Exception as e:
                log.error(
                    "Jinja2 renderer failed to load template: {}; error: {}".format(
                        template_name, e
                    )
                )    
                continue
        
        # render data
        try:
            result[result_name].append(
                templates_objects_dict[template_name].render(datum)
            )
        except Exception as e:
            log.error(
                "Jinja2 renderer failed to render template: {}; error: {}; data: {}".format(
                    template_name, e, datum
                )
            )    
    # transform results into strings
    for result_name, result_list in result.items():
        result[result_name] = "\n".join(result_list)
        del(result_list)
        
    return result
