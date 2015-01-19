# coding: utf-8

from solute.epfl.core.epflcomponentbase import ComponentContainerBase
from solute.epfl.components import ToggleListLayout, cfButton
from solute.epfl.core import epflutil
from solute.epfl.core import epfli18n
import copy
from jinja2 import filters as jinja_filters


class TreeLayout(ComponentContainerBase):

    compo_state = ComponentContainerBase.compo_state + ['show_children']
    js_parts = ComponentContainerBase.js_parts + ["tree_layout/tree_layout.js"]

    theme_path = ['tree_layout/theme']

    data_interface = {'id': None,
                      'children': None,
                      'show_children': None,
                      'label': None}

    label = None
    id = None
    children = []
    show_children = False

    def handle_show(self):
        self.show_children = True
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        self.redraw()
