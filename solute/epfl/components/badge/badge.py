# coding: utf-8


from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Badge(epflcomponentbase.ComponentBase):

    template_name = "badge/badge.html"
    js_name = "badge/badge.js"

    asset_spec = "solute.epfl.components:badge/static"
    js_name = ["badge.js"]

    css_name = ["badge.css", "bootstrap.min.css"]

    compo_state = ["value"]

    compo_config = []
    
    value = None
    

