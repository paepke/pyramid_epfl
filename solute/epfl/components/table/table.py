# coding: utf-8

"""
A table component.
The python part.

jqgrid is used on the client side:

http://www.trirand.com/jqgridwiki/

Maybe you need further customisation - what is possible can be checked out at:

http://www.trirand.com/jqgridwiki/doku.php?id=wiki%3aoptions

If you need something new, you must modify the table.html-template (especially the init_js-part) yourself (and introduce new class-attributes for your
changes of course!)


TODO:

Save state for:
    display/hide-table
    scroll_pos

Data-Types
    str vs html
    Date
    icon
    checkbox
    button
editing?
action-buttons
row-clicks
selecting


"""

import math

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil

from jinja2 import filters as jinja_filters


class Table(epflcomponentbase.ComponentBase):

    template_name = "table/table.html"
    asset_spec = "solute.epfl.components:table/static"
    exporting_macros = ["table", "pager"]

    js_name = ["jquery.jqGrid-4.4.1/js/i18n/grid.locale-de.js",
               "jquery.jqGrid-4.4.1/js/jquery.jqGrid.src.js",
               "table.js"]

    css_name = ["jquery.jqGrid-4.4.1/css/ui.jqgrid.css",
                "table.css"]

    compo_state = ["start_row",
                   "num_rows",
                   "sort_column",
                   "sort_order",
                   "col_widths",
                   "scroll_pos",
                   "table_shown",
                   "target_row_id"]

    compo_config = ["columns_def"]

    # table config:
    caption = "A Table"                             # the caption of the table
    columns_def = []                                # the definition of the columns (a list of dicts)
                                                    #
                                                    # [{"name": ..., "type": "id", ...},
                                                    #  {"name": ..., "type": "text", ...}]
                                                    #
                                                    # some keys accepted in the col-def:
                                                    #
                                                    # name, label, sortable, resizable, default
                                                    #
                                                    # if you omit the "label" then "hidden" will be set to true.
                                                    #
                                                    # For a complete list of possible keys in the dict look here:
                                                    # http://www.trirand.com/jqgridwiki/doku.php?id=wiki:colmodel_options
                                                    #
                                                    # Supported types are:
                                                    # "text": Simply displays the cell-value
                                                    # "id": Same as "text" but the cell-value is used as id for the complete row and must be unique for the table
                                                    # "icon": cell-value must be a dict with the keys
                                                    #         "src": the icon-src
                                                    #         "link": the link-target as url
                                                    #         "tip": [optional] the tooltip for this icon
                                                    # "anchor": cell-value must be a dict with the keys
                                                    #           "href": the link
                                                    #           "name": [optional] name to be displayed, if not specified href will be used
                                                    #           "target": [optional] if you need to open the link in a new tab
                                                    #           "class": [optional] set css style class for the link
                                                    #           "style": [optional] set css style directly on the anchor element
                                                    #
                                                    #
    total_rows_known = True                         # Set this to "False" if your data-source can not calculate
                                                    # the total number of rows (first part of return-value)
    num_rows = 20                                   # the number of rows initially displayed to the user
    num_rows_domain = [10, 20, 50, 100, 'Alle']     # the user can choose to display these number of rows
    sort_column = None                              # the column-name sorted by (or None)
    sort_column_default = None    
    sort_order = "asc"                              # the initial sort order ("asc" / "desc")
    sort_order_default = None    
    table_data_url = ""                             # the url called to read the data (should be "")
    width = "max"                                   # the width of the table: "max" or an integer (pixel)
    height = 150                                    # the heigth of the table: in integer (pixel)

    start_row = 0                                   # Display the data from this row on
    col_widths = {}                                 # internal storage for resized columns
    scroll_pos = 0, 0                               # top and left-scroll-pos of the table
    table_shown = True                              # indicates if the table is fold out or not

    on_row_click = None                             # the name of the event fired, when clicked on a row

    # internal
    target_row_id = None

    multisort = False

    def setup_component(self):
        super(Table, self).setup_component()

        # handle "autowidth"-feature
        if self.width == "max":
            self.autowidth = True
            self.width = "undefined"
        else:
            self.autowidth = False

        idx_name = None

        for column_def in self.columns_def:

            col_type = column_def["type"]
            col_name = column_def["name"]

            # col-type and "id"
            if col_type == "id":
                if idx_name:
                    raise ValueError("Table can not define two 'id'-columns")
                column_def["id"] = True
                idx_name = column_def["name"]
            else:
                column_def["id"] = False

            if col_type == "icon":
                col_type = "text"
                column_def["formatter"] = "icon_formatter"

            if col_type == "anchor":
                col_type = "text"
                column_def["formatter"] = "anchor_formatter"

            # fixed, resized columns:
            if col_name in self.col_widths:
                column_def["width"] = self.col_widths[col_name]

            # handle "fixed"-feature
            if column_def.get("width") == "max":
                column_def["fixed"] = False
                del column_def["width"]
            elif column_def.get("width"):
                column_def["fixed"] = True
            column_def["index"] = column_def["name"]

            if "label" not in column_def:
                column_def["hidden"] = True



##            # i18n
##            if "label" in column_def:
##                column_def["label"] = epfli18n.get_text(column_def["label"])

        if not idx_name:
            raise ValueError("Table must define exaclty one 'id'-column")

        self.index_column_name = idx_name

        # page_nr
        if self.num_rows:
            self.current_page = int(self.start_row / self.num_rows) + 1
        else:
            self.current_page = 0

        if not self.total_rows_known:
            self.pager_template = "{0}"
        else:
            self.pager_template = None

        if self.sort_column:
            self.sort_column_default = self.sort_column

        self.sort_order_default = self.sort_order

    def idx2colum_name(self, idx):
        if idx is None:
            return None
        return self.columns_def[idx]["name"]

    def getTargetRowId(self):
        """ This is the row-id (the value of the cell with type='id') from the row which was selected last
        by the user """
        return self.target_row_id

    def getData(self, start_row, num_rows, sort_column, sort_order):
        """ Dummy function. Please overwrite me! """
        return 0, []

    def refresh_data(self):
        """ Call this if you want to refresh the data in the browser """
        js = "epfl.components[\"" + self.cid + "\"].refresh_data();"
        self.add_ajax_response(js)

    def handle_getData(self, num_rows, page, sort_column, sort_order):
        """ Called from the system when the frontend needs the data of the datatable.
        This handler it self calls the "getData"-Method which returns the data.
        """

        self.num_rows = num_rows

        if num_rows:
            self.start_row = (page - 1) * self.num_rows
        else:
            self.start_row = 0

        sort_param = None
        if self.multisort and isinstance(sort_column, dict):
            sort_param = sorted([(key, val[0], val[1]) for key, val in sort_column.items()], key=lambda x: x[2])
        else:
            sort_param = self.idx2colum_name(sort_column)    

        self.sort_order = sort_order

        # really reading the data...
        total_rows, data = self.getData(start_row=self.start_row,
                                        num_rows=self.num_rows,
                                        sort_column=sort_param,
                                        sort_order=self.sort_order)

        # adding default values
        for col_def in self.columns_def:
            default = col_def.get("default")
            col_name = col_def["name"]
            if default:
                for row in data:
                    if col_name not in row:
                        row[col_name] = default
                    elif type(default) is dict:
                        row[col_name] = dict(default, **row[col_name])  # merge default dict
            if col_def['type'] == u'icon':
                for row in data:
                    src = row[col_name].get("src")
                    if src and src[:4] != "http":
                        src = self.request.static_url(src)
                        row[col_name]["src"] = src
                    tip = row[col_name].get("tip")
                    if tip:
                        tip = jinja_filters.do_striptags(tip)
##todo                        tip = epfli18n.get_text(tip)
                        row[col_name]["tip"] = tip
            if col_def['type'] == u'anchor':
                for row in data:
                    name = row[col_name].get("name")
                    if not name:
                        name = row[col_name].get("href")
                        row[col_name]["name"] = name

                    target = row[col_name].get("target")
                    if not target:
                        target = "_self"
                        row[col_name]["target"] = target

        # converting to the format needed by jqgrid...
        col_keys = [cd["name"] for cd in self.columns_def]
        transformer = epflutil.make_dict2list_transformer(col_keys)

        rows = []
        for row in data:
            trans_row = transformer(row)
            rows.append({"cell": trans_row})

        # handling internal state...
        if self.num_rows:
            self.current_page = int(self.start_row / self.num_rows) + 1

            if total_rows is not None:
                total_pages = int(math.ceil(float(total_rows) / self.num_rows))
                if total_pages == 0:
                    total_pages = 1
            else:
                total_pages = None
        else:
            self.current_page = 0
            total_pages = 1

        out = {"total": total_pages,
               "page": self.current_page,
               "records": total_rows,
               "rows": rows}

        self.response.answer_json_request(out)

    def handle_setColumnWidth(self, col_idx, new_width):
        """ Called by the system, when the user resizes a column.
        The event is queued on client side, so this function will not be called directly after the user interaction
        but some time after that.
        """

        col_name = self.columns_def[col_idx]["name"]
        self.col_widths[col_name] = new_width

    def handle_setScrollPos(self, top, left):
        """ Called by the system, when the user scrolls the table in the browser.
        (this is an repeatedly-enqueued event)
        """
        self.scroll_pos = top, left

    def handle_foldTable(self, table_shown):
        """ Called by the system, when the user clicks on the table-header and hides/unhides the table.
        (this is an repeatedly-enqueued event)
        """
        self.table_shown = table_shown

    def handle_setTargetRowId(self, row_id):
        self.target_row_id = row_id

