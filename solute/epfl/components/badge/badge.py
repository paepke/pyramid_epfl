# coding: utf-8


from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.core import epflutil


class Badge(ComponentBase):
    """
    Simple Badge Compo uses bootstrap badge

    example: http://getbootstrap.com/components/#badges
    """

    template_name = "badge/badge.html"
    js_name = "badge/badge.js"

    asset_spec = "solute.epfl.components:badge/static"
    js_name = ["badge.js"]

    css_name = ["badge.css"]

    compo_state = ["value"]

    compo_config = []
    
    value = None
    

