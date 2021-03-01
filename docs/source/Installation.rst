Installation
############

From PyPi::

    python3 -m pip install py-ttr
  
Make sure that TTR installed using Python version 3.6 or higher.
  
Or latest code from GitHub master branch::

    python3 -m pip install git+https://github.com/dmulyalin/template-text-renderer
  
But for this to work need to have git installed on the system.
  
As part of installation TTR will automatically install these libraries::

    PyYAML>=5.3.1
    openpyxl>=3.0.4
    Jinja2>=2.11.2
    
Alternatively, if you planning to use TTR as a CLI utility only, for Windows you can download
``ttr.exe`` file from `GitHub repository <https://github.com/dmulyalin/template-text-renderer/>`_
`Executable` folder and use it as a CLI tool. **No Python required on the system in that case**, all 
dependencies packed within ``ttr.exe`` executable.