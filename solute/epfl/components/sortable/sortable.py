# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
import json

class Sortable(epflcomponentbase.ComponentBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "sortable/sortable.html"
    js_parts = "sortable/sortable.js"
    asset_spec = "solute.epfl.components:sortable/static"

    css_name = ["sortable.css"]
    js_name = ["sortable.js"]

    
    compo_config = []
    compo_state = ["sort_order","child_components"]

    sort_order = []
    child_components = []
    
    def handle_orderChanged(self,newOrder):
        self.sort_order = newOrder
        self.make_order()

    def make_order(self):
        if self.sort_order:
            js = "epfl.components[\"" + self.cid + "\"].makeSortOrder("+json.dumps(self.sort_order)+");"
            self.add_ajax_response(js)
    
    def handle_loadingFinished(self):
        self.make_order()

    def get_sort_order(self):
        return self.sort_order

    def set_sort_order(self, new_order):
        self.sort_order = new_order
        self.make_order()
    
    def add_child_component(self,name, child):
        self.child_components.append({ "name" : name, "element" : child })
