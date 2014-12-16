# coding: utf-8


from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Button(epflcomponentbase.ComponentBase):

    template_name = "button/button.html"

    asset_spec = "solute.epfl.components:button/static"
    js_name = ["button.js"]

    css_name = ["button.css", "bootstrap.min.css"]

    compo_state = []

    compo_config = []
    
    label = ""

    # Overwrite me
    def handle_on_click(self):
        pass
    

