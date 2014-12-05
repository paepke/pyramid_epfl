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
