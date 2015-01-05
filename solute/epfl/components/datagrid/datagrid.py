# coding: utf-8
from solute.epfl.core import epflcomponentbase

class DataGrid(epflcomponentbase.ComponentBase):

    template_name = "datagrid/datagrid.html"
    js_parts = "datagrid/datagrid.js"

    asset_spec = "solute.epfl.components:datagrid/static"

    js_name = ["bootstrap-table.js","highcharts.js"]
    css_name = ["datagrid.css","bootstrap.min.css","bootstrap-table.css"]

    compo_state = ["data_url"]

    compo_config = []

    #Overwrite these !
    data_url = ""
    fields = []

    #General Settings
    height = 400
    data_search = True
    card_view = False

    #Pagination Settings
    pagination = True
    page_list = "[5, 10, 20, 50, 100, 200]"
    page_size = 10


    def handle_getdata(self):
        print "GET DATA"