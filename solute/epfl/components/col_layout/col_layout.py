# coding: utf-8

"""

"""
from solute.epfl.core import epflcomponentbase


class ColLayout(epflcomponentbase.ComponentContainerBase):
    
    asset_spec = "solute.epfl.components:col_layout/static"
    css_name = ["col_layout.css"]
    
    template_name = "col_layout/col_layout.html"
    vertical_center = False
