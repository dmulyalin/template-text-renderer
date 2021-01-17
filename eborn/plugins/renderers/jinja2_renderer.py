import logging
import jinja2
import os

log = logging.getLogger(__name__)


def render(
        data, 
        template_name_key,
        templates_dir, 
        templates_dict, 
        result_name_key,
        **renderer_kwargs
    ):
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
        if template_name in templates_dict:
            template_content = templates_dict[template_name]
        else:
            template_file_path = os.path.join(
                templates_dir, template_name if template_name.endswith(".txt") else "{}.txt".format(
                    template_name
                )
            )
            if os.path.isfile(template_file_path):
                with open(template_file_path, "r") as f:
                    template_content = f.read() 
            else:
                log.error(
                    "Jinja2 renderer failed to open template file: '{}'".format(
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
