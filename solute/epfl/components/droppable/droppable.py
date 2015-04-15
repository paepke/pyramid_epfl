from solute.epfl.core import epflcomponentbase
from solute.epfl.components.dragable.dragable import Dragable
import json


class Droppable(epflcomponentbase.ComponentContainerBase):
    template_name = "droppable/droppable.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["droppable/droppable.js"]
    asset_spec = "solute.epfl.components:droppable/static"

    css_name = ["droppable.css"]
    js_name = ["droppable.js"]

    compo_config = epflcomponentbase.ComponentContainerBase.compo_config + ["valid_types"]
    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + ["elements", "is_collapsed", "title", "is_selected"]

    valid_types = [Dragable]
    elements = [] # TODO: should be set to None since it is in compo_state
    collapsable = False
    title_renamable = False
    is_selected = False # TODO: should be set to None since it is in compo_state
    selectable = False # TODO: should be set to None since it is in compo_state
    is_collapsed = False # TODO: should be set to None since it is in compo_state
    title = None
    # if set to true, a child cannot be dragged once it has been placed inside
    # the droppable
    deactivate_on_drop = False

    def init_transaction(self):
        super(Droppable, self).init_transaction()
        if (self.collapsable == True) and (self.title is None):
            raise RuntimeError("Title must be set for collapsable droppables!")

    def add_dragable_element(self, element, position=None):
        if not hasattr(element, 'cid') or not hasattr(self.page, element.cid):
            element = self.add_component(element)
        if position is not None:
            self.switch_component(self.cid, element.cid, position=position)
        self.redraw()

    def handle_add_dragable(self, cid, position):
        self.switch_component(self.cid, cid, position=position)

    def handle_toggle_collapse(self, collapsed):
        self.is_collapsed = collapsed

    def handle_rename_title(self, title):
        self.title = title

    def get_valid_types(self, dotted=False):
        if dotted:
            return json.dumps(['.droppable_type_%s' % t.type for t in self.valid_types])
        return ' '.join(['droppable_type_%s' % t.type for t in self.valid_types])


class SimpleDroppable(epflcomponentbase.ComponentContainerBase):
    template_name = "droppable/simpledroppable.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts[:]
    js_parts.append("droppable/simpledroppable.js")
    asset_spec = "solute.epfl.components:droppable/static"

    css_name = ["simpledroppable.css"]
    js_name = ["simpledroppable.js"]

    compo_config = ["valid_types"]
    compo_state = ["elements", "title"]

    valid_types = [Dragable]
    elements = [] # TODO: should be set to None since it is in compo_state

    title = None
    is_content_removable = False

    def handle_remove_content(self):
        if len(self.components) > 0:
            for comp in self.components:
                comp.delete_component()

    def get_valid_types(self, dotted=False, as_json=False):
        if dotted:
            if as_json:
                return json.dumps(['.droppable_type_%s' % t.type for t in self.valid_types])
            return ' '.join(['.droppable_type_%s' % t.type for t in self.valid_types])
        if as_json:
            return json.dumps(['droppable_type_%s' % t.type for t in self.valid_types])
        return ' '.join(['droppable_type_%s' % t.type for t in self.valid_types])
