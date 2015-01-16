# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Panel(epflcomponentbase.ComponentContainerBase):


    template_name = "panel/panel.html"
    asset_spec = "solute.epfl.components:panel/static"

    css_name = ["panel.css"]

