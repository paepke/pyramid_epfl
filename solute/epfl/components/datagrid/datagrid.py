# coding: utf-8
from solute.epfl.core import epflcomponentbase

class DataGrid(epflcomponentbase.ComponentBase):

    template_name = "datagrid/datagrid.html"
    js_parts = "datagrid/datagrid.js"

    asset_spec = "solute.epfl.components:datagrid/static"
    js_name = ["datagrid.js",
               "jqgrid-4.7.1/js/i18n/grid.locale-de.js",
               "jqgrid-4.7.1/js/jquery.jqGrid.src.js"]

    css_name = ["datagrid.css", "jqgrid-4.7.1/css/ui.jqgrid.css","bootstrap.min.css"]

    compo_state = []

    compo_config = []

    def handle_getdata(self):
        print "GET DATA"