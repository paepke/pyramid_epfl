# coding: utf-8
from solute.epfl.core import epflcomponentbase



class Modal(epflcomponentbase.ComponentContainerBase):

    template_name = "modal/modal.html"
    
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["modal/modal.js"]

    asset_spec = "solute.epfl.components:modal/static"

    js_name = []
    css_name = ["bootstrap.min.css"]

    compo_state = ["title"]

    compo_config = []

    title = ""





