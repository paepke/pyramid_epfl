# coding: utf-8

"""

"""
from solute.epfl.core import epflcomponentbase


class Dropdown(epflcomponentbase.ComponentBase):

    asset_spec = "solute.epfl.components:dropdown/static"

    js_parts = ["dropdown/dropdown.js"]
    js_name = ["dropdown.js"]

    template_name = "dropdown/dropdown.html"
    small_button = True  #: Use a small button for the dropdown menu
    caret = False  #: Show a caret indicator on the dropdown menu button
    #: The label of the dropdown menu button. Optional, if a :attr:`menu_icon` is provided.
    menu_label = None
    #: Optional font-awesome icon to be rendered as menu_label.
    # If both :attr:`menu_icon` and :attr:`menu_label` are provided, the icon
    # is rendered before the label.
    menu_icon = None
    children = []
