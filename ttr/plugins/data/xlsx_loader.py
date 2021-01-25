"""
XLSX Spreadsheets loader plugin
*******************************

**Plugin Name:** ``xlsx``

This plugin supports loading data from multiple sheets, combining them for rendering.

**Prerequisites:**

- Requires `openpyxl <https://pypi.org/project/openpyxl/>`_ library

Spreadsheets must contain a column or multiple columns with headers starting
with ``template_name_key`` argument string. Values of template(s) columns either
names of the template to use for rendering or OS path string to template file
relative to ``template_dir`` argument supplied to TTR object on instantiation.

In addition, table must contain column with ``result_name_key`` values, they used
to combine results, i.e. rendering results for identical ``result_name_key`` combined
in a single string. ``result_name_key`` used further by returners to return results.

Spreadsheet might contain multiple tabs with names starting with ``template``, these
tabs can contain templates to use for rendering data from other tabs. All the templates
loaded line by line, ``template:{{ template_name }}`` lines used to identify end
of previous and start of next template, where ``template_name`` used for referencing
template in templates columns.
"""

import logging
from openpyxl import load_workbook

log = logging.getLogger(__name__)


def load_template(sheet, templates_dict):
    log.debug("XLSX loader, loading templates tab - '{}'".format(sheet.title))
    current_template_name = ""
    current_template_lines = []
    for item in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
        rowData = item[0]
        if rowData != None:  # check if cell is empty and skip it if so
            if rowData.upper().startswith("TEMPLATE:"):
                if current_template_lines and current_template_name:
                    templates_dict[current_template_name] = "\n".join(
                        current_template_lines
                    )
                current_template_name = rowData.split(":")[1].strip()
                current_template_lines = []
            else:
                current_template_lines.append(rowData)
    # add last template
    if current_template_lines and current_template_name:
        templates_dict[current_template_name] = "\n".join(current_template_lines)


def load_data_from_sheet(sheet, ret, template_name_key):
    headers = [
        sheet.cell(row=1, column=i).value for i in range(1, sheet.max_column + 1)
        if not sheet.cell(row=1, column=i).value.startswith("#")
    ]

    has_templates_column = False
    for header in headers:
        if header.startswith(template_name_key):
            has_templates_column = True
            break

    if not has_templates_column:
        log.warning(
            "XLSX loader, no '{}' header on tab '{}', skipping it".format(
                template_name_key, sheet.title
            )
        )
        return

    # form data
    log.debug("XLSX loader, loading data - tab: '{}', headers: '{}'".format(sheet.title, headers))
    for row in sheet.iter_rows(min_row=2, values_only=True):
        ret.append(
            dict(zip(headers, row))
        )


def load(data, templates_dict, template_name_key, **kwargs):
    """
    Function to load XLSX spreadsheet. Takes OS path to ``.xlsx`` file
    and returns list of dictionaries, where keys equal to headers
    of spreadsheets' tabs.

    :param data: string, OS path to ``.xlsx`` file
    :param templates_dict: dictionary to load templates from spreadsheet
    :param template_name_key: string, templates column header prefix
    """
    ret = []

    kwargs.setdefault("data_only", True)
    kwargs.setdefault("read_only", True)

    wb = load_workbook(data, **kwargs)

    for sheet_name in wb.sheetnames:
        if sheet_name.startswith("#"):
            log.debug("XLSX loader, skipping tab - '{}'".format(sheet_name))
            continue
        elif "TEMPLATE" in sheet_name.upper():
            load_template(wb[sheet_name], templates_dict)
        else:
            load_data_from_sheet(wb[sheet_name], ret, template_name_key)
    return ret
