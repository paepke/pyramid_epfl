# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class ColLayout(epflcomponentbase.ComponentTreeBase):

    template_name = "layout/col.html"
    asset_spec = "solute.epfl.components:layout/static"

    css_name = ["bootstrap.min.css"]
