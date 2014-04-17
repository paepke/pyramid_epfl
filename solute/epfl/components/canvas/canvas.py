# coding: utf-8

"""

"""

import types, copy

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Canvas(epflcomponentbase.ComponentBase):

    template_name = None

    asset_spec = "solute.epfl.components:canvas/static"
    js_name = ["canvas.js"]

    css_name = []

    compo_state = []

    compo_config = []



    def pre_render(self):
        """ Overwrite me and set some template attributes to self """
        super(Canvas, self).pre_render()


