# coding: utf-8
from solute.epfl.core import epflcomponentbase

class Progress(epflcomponentbase.ComponentBase):

    template_name = "progress/progress.html"
    
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["progress/progress.js"]

    asset_spec = "solute.epfl.components:progress/static"
    js_name = ["progress.js"]

    css_name = ["progress.css", "bootstrap.min.css"]

    compo_state = ["value","min","max"]

    compo_config = []

    value = 0
    min = 0
    max = 100