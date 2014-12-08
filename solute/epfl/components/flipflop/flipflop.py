# coding: utf-8


"""

"""

import types, copy

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil

from pyramid import security

class FlipFlop(epflcomponentbase.ComponentBase):
    __acl__ = [(security.Allow, security.Everyone, 'access')] 
    template_name = "flipflop/flipflop.html"

    asset_spec = "solute.epfl.components:flipflop/static"
    js_name = ["jquery.tablednd.js", "flipflop.js"]

    css_name = ["flipflop.css", "bootstrap.min.css"]

    compo_state = ["sortorder"]

    compo_config = []
    
    sortorder= []



