# coding: utf-8

from solute.epfl.core.epflcomponentbase import ComponentContainerBase, ComponentBase
from solute.epfl.components import ToggleListLayout, DragBox
from solute.epfl.core import epflutil
from solute.epfl.core import epfli18n
import copy
from jinja2 import filters as jinja_filters


class DraggableTreeLeafEntry(DragBox):
    theme_path = ["tree_layout/dragable_tree_leaf_entry_theme"]
    label = None
    icon = None

    compo_state = ["label", "icon"]


class TreeLeafEntry(ComponentBase):
    template_name = "tree_layout/tree_leaf_entry.html"
    label = None
    icon = None

    compo_state = ["label", "icon"]


class TreeLayout(ComponentContainerBase):

    asset_spec = "solute.epfl.components:tree_layout/static"
    css_name = ["tree_layout.css"]

    compo_state = ComponentContainerBase.compo_state + \
        ['tree_node_dict', 'expanded_nodes']
    js_parts = ComponentContainerBase.js_parts + ["tree_layout/tree_layout.js"]

    theme_path = ['tree_layout/theme']

    data_interface = {'id': None,
                      'label': None,
                      'number_of_children': None}

    label = None
    id = None
    #: the number of children for this tree. If the tree is collapsed, its child components 
    # need not to be set, but this field can be used to indicate whether the node has children.
    number_of_children = None
    
    max_height = None #: Set the max height of the tree (optional). If the tree has more contents, scroll bars are used
    min_height = None #: Set the min height of the tree (optional).

    @property
    def show_children(self):
        return self.row_data.get("show_children", False)

    @show_children.setter
    def show_children(self, show_children):
        self.row_data["show_children"] = show_children

    # : Specify a custom font-awesome icon class for collapsed nodes.
    custom_node_icon_collapsed = None
    # : Specify a custom font-awesome icon class for expanded nodes.
    custom_node_icon_expanded = None
    # : Specify a custom font-awesome icon class for empty nodes (no child components).
    empty_node_icon = None

    #: Indicates a set filter that can be used by get_data to return filtered entries only
    #: This dict can store the data of the root nodes of this tree for caching: TreeModelBase respects this.
    tree_node_dict = {}
    #: Store the ids of expanded nodes, can be used by model, but is not set automatically.
    expanded_nodes = []

    # folder icons
    # custom_node_icon_collapsed="fa-folder-o"
    # custom_node_icon_expanded="fa-folder-open-o"

    def handle_show(self):
        self.show_children = True
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        self.redraw()

    def is_smart(self):
        """
        If show_children is false, this tree is regarded as a non-smart component.
        In this case, all child elements returned by get_data won't be regarded
        """
        return ComponentContainerBase.is_smart(self) and self.show_children

    def update_children_recursively(self):
        self.update_children(force=True)

        for c in self.components:
            try:
                c.update_children_recursively()  # also a tree
            except AttributeError:
                try:
                    c.update_children(force=True)
                except AttributeError:
                    pass  # a base component


class DroppableTreeLayout(TreeLayout):

    js_name = TreeLayout.js_name + ["droppable_tree_layout.js"]
    js_parts = TreeLayout.js_parts + ['tree_layout/droppable_tree_layout.js']

    def handle_drag_stop(self, position=None, cid=None, over_cid=None):
        pass

    def handle_drop_accepts(self):
        pass
