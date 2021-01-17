"""
EBORN CLI tool
==============

This tool can be used to render data from various sources and either
print results to screen or save them in output folder.

Supported arguments::

    -d,  --data          OS path to folder with data files or to data file, default ./Data/
    -t,  --templates     OS path to folder with templates, default ./Templates/
    -o,  --output        Output folder location, default ./Output/{{ current time }}/
    -p,  --print         Print results to terminal instead of saving to folder
"""
import argparse
import time
import os
import logging

log = logging.getLogger(__name__)


#if run as a script, inject eBORN folder in system path
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')

from eborn import eborn

__version__ = "0.1.0"
ctime = time.strftime("%Y-%m-%d_%H-%M-%S")

cli_help = """
Extendable Bulk Configuration Generator

-d,  --data          OS path to folder with data files or to data file, default ./Data/
-t,  --templates     OS path to folder with templates, default ./Templates/
-o,  --output        Output folder location, default ./Output/{{ current time }}/
-p,  --print         Print results to terminal instead of saving to folder
"""

def cli_tool():
    # form argparser menu:
    description_text = """{}""".format(cli_help)

    argparser = argparse.ArgumentParser(
        description="eBORN CLI, version {}".format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    run_options = argparser.add_argument_group(description=description_text)
    #-----------------------------------------------------------------------------
    # General options
    #-----------------------------------------------------------------------------
    run_options.add_argument(
        "-d",
        "--data",
        action="store",
        dest="DATA",
        default="./Data/",
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-t",
        "--templates",
        action="store",
        dest="TEMPLATES_FOLDER",
        default="./Templates/",
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-o",
        "--output",
        action="store",
        dest="OUTPUT_FOLDER",
        default='./Output/{}_{{}}/'.format(ctime),
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-p",
        "--print",
        action="store_true",
        dest="PRINT_TO_TERMINAL",
        default=False,
        help=argparse.SUPPRESS,
    )
    
    #-----------------------------------------------------------------------------
    # Parse arguments
    #-----------------------------------------------------------------------------
    args = argparser.parse_args()

    # general arguments
    DATA = args.DATA  # string, OS path to data file or folder with files to process
    TEMPLATES_FOLDER = args.TEMPLATES_FOLDER  # OS path to folder to save results into
    OUTPUT_FOLDER = args.OUTPUT_FOLDER  # output filename
    PRINT_TO_TERMINAL = args.PRINT_TO_TERMINAL

    # get data file OS path
    if os.path.isdir(DATA):
        # get the list of files in 'Data' folder
        data_files = os.listdir(DATA)  
        if len(data_files) == 1:
            file_number = 0
        elif len(data_files) == 0:
            log.error("No files found in 'Data' directory; Exiting...")
            raise SystemExit()
        # if more than one file found, ask user which file to use
        else:
            print("{}\nFiles found in '{}' directory".format(20 * "=", DATA))  
            for position, item in enumerate(data_files):
                print("{}: {}".format(position, item))
            # get file number to work with
            file_number = -1
            while not(0 <= file_number <= len(data_files) - 1):
                try:
                    file_number = int(input("Choose data file to work with (number): "))
                except KeyboardInterrupt:
                    raise SystemExit()
                except:
                    continue
        # form path to data file
        data_file_path = os.path.join(DATA, data_files[file_number])
    elif os.path.isfile(DATA):
        data_file_path = DATA
        
    if not PRINT_TO_TERMINAL and not os.path.exists(OUTPUT_FOLDER):
        OUTPUT_FOLDER = OUTPUT_FOLDER.format(
            os.path.split(data_file_path)[-1]
        )
        os.makedirs(OUTPUT_FOLDER)
        
    # generate results and save them in output folder or print to screen
    with eborn(
            data=data_file_path, 
            templates_dir=TEMPLATES_FOLDER,
            returner="terminal" if PRINT_TO_TERMINAL else "file", 
            returner_kwargs={
                "result_dir": OUTPUT_FOLDER
            }
    ) as g:
        g.run()

if __name__ == "__main__":
    cli_tool()
