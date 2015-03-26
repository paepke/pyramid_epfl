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
    keep_orig_in_place = True # TODO: is that okay? (None default since it is in compo state

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
        ['tree_node_dict', 'expanded_nodes', 'show_children', 'selected']
    js_name = ["tree_layout.js"]
    js_parts = ComponentContainerBase.js_parts + ["tree_layout/tree_layout.js"]

    theme_path = ['tree_layout/theme']
    template_name = 'tree_layout/tree_layout_base.html'

    data_interface = {'id': None,
                      'label': None,
                      'number_of_children': None}

    label = None
    id = None
    #: the number of children for this tree. If the tree is collapsed, its child components
    # need not to be set, but this field can be used to indicate whether the node has children.
    number_of_children = None
    
    show_children = False #: Set to true if child entries of the tree should be shown.
    selected = False #: Set to true if element should be marked as selected.

    #: Set the max height of the tree (optional). If the tree has more contents, scroll bars are used
    max_height = None
    min_height = None  #: Set the min height of the tree (optional).

    #: This dict stores the child components in its slots. All default components, i.e. all tree children nodes,
    # end up in the "children" slot. A context menu can be placed in the "context_menu" slot.
    _slotted_components = None

    # : If set to true, the context menu is only visible when the mouse hovers over the tree entry.
    show_context_menu_on_hover_only = False

    #: Return a subset of the tree's child components, based on the given slot type.
    def slotted_components(self, slot_type='children'):
        #print "CALL slotted_components on comp %r, %r child compos." % (self.cid, len(self.components))
        #print " _slotted_components: %r" % self._slotted_components
        if self._slotted_components is None:
            self._slotted_components = {'children': [],
                                        'context_menu': []}
            for compo in self.components:
                #print "CHECK: " + str(type(compo)) + " | " + repr(getattr(compo, 'container_slot', None))
                self._slotted_components.setdefault(
                    getattr(compo, 'container_slot', None) or 'children', []).append(compo)

        return self._slotted_components.get(slot_type, [])

    # : Specify a custom font-awesome icon class for collapsed nodes.
    custom_node_icon_collapsed = None
    # : Specify a custom font-awesome icon class for expanded nodes.
    custom_node_icon_expanded = None
    # : Specify a custom font-awesome icon class for empty nodes (no child components).
    empty_node_icon = None

    #: Indicates a set filter that can be used by get_data to return filtered entries only
    #: This dict can store the data of the root nodes of this tree for caching: TreeModelBase respects this.
    tree_node_dict = None
    #: Store the ids of expanded nodes, can be used by model, but is not set automatically.
    expanded_nodes = None

    # folder icons
    # custom_node_icon_collapsed="fa-folder-o"
    # custom_node_icon_expanded="fa-folder-open-o"

    def handle_show(self):
        self.show_children = True
        for compo in self.components:
            compo.set_visible()
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        for compo in self.components:
            compo.set_hidden()
        self.redraw()

    def is_smart(self):
        """
        If show_children is false, this tree is regarded as a non-smart component.
        In this case, all child elements returned by get_data won't be regarded
        """
        return ComponentContainerBase.is_smart(self) and self.show_children

    def update_children_recursively(self):
        self.update_children(force=True)
        # don't recursively update children if component is not smart
        # otherwise, show_children might be false, child components are not rendered
        # but they will be updated in a recursion step here.
        if not self.is_smart():
            return
        for c in self.components:
            try:
                c.update_children_recursively()  # also a tree
            except AttributeError:
                try:
                    c.update_children(force=True)
                except AttributeError:
                    pass  # a base component

    def update_children(self, *args, **kwargs):
        ComponentContainerBase.update_children(self, *args, **kwargs)
        self._slotted_components = None


class DroppableTreeLayout(TreeLayout):

    js_name = TreeLayout.js_name + ["droppable_tree_layout.js"]
    js_parts = TreeLayout.js_parts + ['tree_layout/droppable_tree_layout.js']

    def handle_drag_stop(self, position=None, cid=None, over_cid=None):
        pass

    def handle_drop_accepts(self):
        pass
