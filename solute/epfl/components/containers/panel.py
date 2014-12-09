# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Panel(epflcomponentbase.ComponentContainerBase):


    template_name = "containers/panel.html"
    asset_spec = "solute.epfl.components:containers/static"

    css_name = ["panel.css"]



