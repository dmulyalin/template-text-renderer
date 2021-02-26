"""
TTR CLI tool
############

TTR CLI is an example of tool built using TTR library.

This tool can be used to render data from various sources and either
print results to screen or save them in output folder.

Supported arguments::

    -d,  --data          OS path to folder with data files or to data file, default ./Data/
    -t,  --templates     OS path to folder, .txt or .xlsx file with template(s), default ./Templates/
    -o,  --output        Output folder location, default ./Output/<current time><data file name>/
    -p,  --print         Print results to terminal instead of saving to folder
    -l,  --logging       Set logging level - "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"; default ERROR
    -f,  --filters       Comma separated list of glob patterns to use for filtering data to render

.. note:: ``--templates`` argument should be a path to folder with templates 
    files within that folder/subfolders or path to ``.xlsx`` spreadsheet file with 
    templates or path to ``.txt`` file with single template content.
    
In general case TTR CLI utility takes data file and templates location references and saves produced results in a subfolder within ``./Output/`` directory, where subfolder name has this format ``./Output/<current time><data file name>/``.

Sample invocation::

    ttr -d ./data/data.yaml
    ttr -d ./data/data.yaml -t ./templates_folder/
    ttr -d ./data/data.yaml -t ./templates/templates_spreadsheet_file.xlsx

Alternatively a path to directory can be provided instead of data file, in that case TTR will scan that path and prompt
user to select file to work with::

    ttr -d ./data/
    ====================
    Files found in './data/' directory
    0: csv_data_1.csv
    1: data.yaml
    2: table_data_1.xlsx
    Choose data file to work with (number): 1


"""
import argparse
import time
import os
import logging
        
log = logging.getLogger(__name__)


#if run as a script, inject ttr folder in system path
if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')

from ttr import ttr

__version__ = "0.3.1"
ctime = time.strftime("%Y-%m-%d_%H-%M-%S")

cli_help = """
Template Text Renderer CLI utility

-d,  --data          OS path to folder with data files or to data file, default ./Data/
-t,  --templates     OS path to folder or file with templates, default ./Templates/
-o,  --output        Output folder location, default ./Output/<current time><data file name>/
-p,  --print         Print results to terminal instead of saving to folder
-l,  --logging       Set logging level - "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"; default ERROR
-f,  --filters       Comma separated list of glob patterns to use for filtering data to render
"""

def cli_tool():
    # form argparser menu:
    description_text = """{}""".format(cli_help)

    argparser = argparse.ArgumentParser(
        description="TTR CLI, version {}".format(__version__),
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
        dest="TEMPLATES_LOCATION",
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
    run_options.add_argument(
        "-l",
        "--logging",
        action="store",
        dest="LOGGING_LEVEL",
        default='ERROR',
        type=str,
        help=argparse.SUPPRESS,
    )
    run_options.add_argument(
        "-f",
        "--filters",
        action="store",
        dest="FILTERS",
        default="",
        type=str,
        help=argparse.SUPPRESS,
    )
    #-----------------------------------------------------------------------------
    # Parse arguments
    #-----------------------------------------------------------------------------
    args = argparser.parse_args()

    # general arguments
    DATA = args.DATA  # string, OS path to data file or folder with files to process
    TEMPLATES_LOCATION = args.TEMPLATES_LOCATION  # OS path to folder to save results into
    OUTPUT_FOLDER = args.OUTPUT_FOLDER  # output filename
    PRINT_TO_TERMINAL = args.PRINT_TO_TERMINAL
    LOGGING_LEVEL = args.LOGGING_LEVEL
    FILTERS = args.FILTERS
    
    # set logging level
    try:
        logging.basicConfig(
            format="%(asctime)s.%(msecs)d [TTR %(levelname)s] %(lineno)d; %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S",
            level=getattr(logging, LOGGING_LEVEL.upper())
        )
    except Exception as e:
        log.error("TTR:cli_tool - Failed to set logging level to '{}', error: {}".format(LOGGING_LEVEL, e))

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
    else:
        log.error("Failed to form data_file_path, data: '{}'".format(DATA))
        return

    if not PRINT_TO_TERMINAL and not os.path.exists(OUTPUT_FOLDER):
        OUTPUT_FOLDER = OUTPUT_FOLDER.format(
            os.path.split(data_file_path)[-1]
        )
        os.makedirs(OUTPUT_FOLDER)

    # generate results and save them in output folder or print to screen
    with ttr(
            data=data_file_path,
            templates=TEMPLATES_LOCATION,
            returner="terminal" if PRINT_TO_TERMINAL else "file",
            returner_kwargs={
                "result_dir": OUTPUT_FOLDER
            },
            processors=["multitemplate", "filtering", "templates_split"],
            processors_kwargs={
                "filters": [i.strip() for i in FILTERS.split(",")]
            }
    ) as g:
        g.run()

if __name__ == "__main__":
    cli_tool()
