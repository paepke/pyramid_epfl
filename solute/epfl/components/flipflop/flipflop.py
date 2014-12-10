# coding: utf-8


"""

"""

import types, copy

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class FlipFlop(epflcomponentbase.ComponentBase):

    template_name = "flipflop/flipflop.html"

    asset_spec = "solute.epfl.components:flipflop/static"
    js_name = ["jquery.tablednd.js", "flipflop.js"]

    css_name = ["flipflop.css", "bootstrap.min.css"]

    compo_state = ["components"]

    compo_config = []
    
    components = []
    
    def handle_onClickChildren(self,compo_id):
        new_compo = []
        for compo in self.components:
            if compo["id"] != compo_id :
                new_compo.append(compo)
        self.components = new_compo
        
        print compo_id
        js = "epfl.components[\"" + self.cid + "\"].remove_row('"+compo_id+"');"
        self.add_ajax_response(js) 
