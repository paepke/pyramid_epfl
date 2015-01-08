# coding: utf-8
from solute.epfl.core import epflcomponentbase,epflutil

from pyramid.response import Response
import json

class DataTable(epflcomponentbase.ComponentContainerBase):

    template_name = "datatable/datatable.html"
    js_parts = "datatable/datatable.js"

    asset_spec = "solute.epfl.components:datatable/static"

    js_name = []
    css_name = ["bootstrap.min.css"]

    compo_state = ["table_data","table_head","title"]

    compo_config = []

    table_data = []
    table_head = []
    title = ""

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        print "DataTable.get_data"
        data = []
        for i in range(0,1000):
            data.append({"id":i,"data":"data " +str(i)})

        return data

    def init_struct(self):
        pass

class TextValue(epflcomponentbase.ComponentBase):
    template_name = "containers/textvalue.html"
    asset_spec = "solute.epfl.components:containers/static"
    value = None
    compo_state = ["value"]