# coding: utf-8
from solute.epfl.core import epflcomponentbase,epflutil

from pyramid.response import Response
import json


class Row(epflcomponentbase.ComponentBase):
    template_name = "datatable/row.html"
    asset_spec = "solute.epfl.components:datatable/static"

    def setup_component(self):
        super(Row,self).setup_component()
        self.id,self.data

class DataTable(epflcomponentbase.ComponentContainerBase):

    template_name = "datatable/datatable.html"
    js_parts = "datatable/datatable.js"

    asset_spec = "solute.epfl.components:datatable/static"

    js_name = []
    css_name = ["bootstrap.min.css"]

    compo_state = ["table_head","title","search"]

    compo_config = []

    table_head = []
    title = ""

    search = True

    default_child_cls=Row

