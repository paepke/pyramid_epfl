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
    asset_spec = "solute.epfl.components:sortable/static"

    css_name = ["sortable.css"]
    js_name = ["sortable.js"]

    
    compo_config = []
    compo_state = ["sort_order"]

    sort_order = []
    
    def setup_component(self):
        super(Sortable, self).setup_component()
        self.make_order()
        
    def handle_orderChanged(self,newOrder):
        self.sort_order = newOrder
        self.make_order()

    def make_order(self):
        if len(self.sort_order) > 0:
            js = "epfl.components[\"" + self.cid + "\"].makeSortOrder("+json.dumps(self.sort_order)+");"
            self.add_ajax_response(js)

