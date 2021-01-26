# Template Text Renderer - TTR

Module to produce text files using templates. Have a look in [documentation](https://template-text-renderer.readthedocs.io) for details or install from [PyPi](https://pypi.org/project/py-ttr/0.1.0/).

# Why?

To simplify process of producing static text files out of templates. 

Why you need TTR? How much time you spent generating configuration files steering in a computer screen, correcting mistakes, manually copying and pasting various parameters? If answer is hours, well..., TTR might be able to save you some time, probably around 70% of what you normally spend on composing text manually.

# How?

Pluggable systems are great, they are expendable, adaptable, re-usable, plugins functionality self contained etc. 

TTR is a pluggable framework, it supports simple work flow of:

    load data -> load templates -> render (combine data with templates) -> get results 

Where each step accompanied with a set of plugins to fulfill in the moment requirements.

# What?

TTR is very general in terms of supported data and templates, providing space for numerous use cases. 

One of such use-cases might be network devices configuration generation - take inventory 
(XLSX LLD or CSV spreadsheets or YAML or you name it), combine it with templates and find 
hundreds of lines of configuration generated in a matter of seconds.

# Contribution

Feel free to submit an issue, report a bug or ask a question, feature requests are welcomed or [buy](https://paypal.me/dmulyalin) Author a coffee
