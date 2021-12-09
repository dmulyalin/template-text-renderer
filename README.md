[![PyPI](https://img.shields.io/pypi/v/py-ttr.svg)](https://pypi.python.org/pypi/py-ttr)
[![PyPI versions](https://img.shields.io/pypi/pyversions/py-ttr.svg)](https://pypi.python.org/pypi/py-ttr)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Downloads](https://pepy.tech/badge/py-ttr)](https://pepy.tech/project/py-ttr)

# Template Text Renderer - TTR

Module to produce text files using templates. Have a look in [documentation](https://template-text-renderer.readthedocs.io) for details or install from [PyPi](https://pypi.org/project/py-ttr/).

# Why?

To simplify process of producing static text files out of templates.

Why you need TTR? How much time you spent generating configuration files steering in a computer screen, correcting mistakes, manually copying and pasting various parameters? If answer is hours, well..., TTR might be able to save you some time, probably around 70% of what you normally spend on composing text manually.

# How?

Pluggable systems are great, they are expendable, adaptable, re-usable, plugins functionality self contained etc.

TTR is a pluggable framework that aims to implement this work flow:

    load data -> process data -> load data models -> validate data -> load templates -> render (combine data with templates) -> get results

Where each step accompanied with a set of plugins to fulfill in the moment requirements.

# What?

TTR is very general in terms of supported data and templates, providing space for numerous use cases.

One of such use-cases might be network devices configuration generation - take inventory
(XLSX LLD or CSV spreadsheets or YAML or you name it), combine it with templates and find
hundreds of lines of configuration generated in a matter of seconds.

# Contribution

Feel free to submit an issue, report a bug or ask a question, feature requests are welcomed or [buy](https://paypal.me/dmulyalin) Author a coffee
