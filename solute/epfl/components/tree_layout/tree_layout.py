# coding: utf-8

from solute.epfl.core.epflcomponentbase import ComponentContainerBase
from solute.epfl.components import ToggleListLayout
from solute.epfl.core import epflutil
from solute.epfl.core import epfli18n
import copy
from jinja2 import filters as jinja_filters


class TreeLayout(ComponentContainerBase):
    
    asset_spec = "solute.epfl.components:tree_layout/static"
    css_name = ["tree_layout.css"]

    compo_state = ComponentContainerBase.compo_state + ['show_children', 'tree_node_dict']
    js_parts = ComponentContainerBase.js_parts + ["tree_layout/tree_layout.js"]

    theme_path = ['tree_layout/theme']

    data_interface = {'id': None,
                      'children_ids': None,
                      'show_children': None,
                      'label': None}

    label = None
    id = None
    children_ids = []
    show_children = False
    custom_node_icon_collapsed=None
    custom_node_icon_expanded=None
    tree_node_dict = {} #: This dict can store the data of the root nodes of this tree for caching: TreeModelBase respects this.
     
    # folder icons
    #custom_node_icon_collapsed="fa-folder-o"
    #custom_node_icon_expanded="fa-folder-open-o"

    def handle_show(self):
        self.show_children = True
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        self.redraw()
