from solute.epfl.core import epflcomponentbase
from solute.epfl.components.dragable.dragable import Dragable
import json


class Droppable(epflcomponentbase.ComponentContainerBase):
    template_name = "droppable/droppable.html"
    asset_spec = "solute.epfl.components:droppable/static"

    css_name = ["droppable.css", "bootstrap.min.css"]
    js_name = ["droppable.js"]

    compo_config = ["valid_types"]
    compo_state = ["elements"]

    valid_types = [Dragable]
    elements = []

    def add_dragable_element(self, element, position=None):
        if not hasattr(element, 'cid') or not hasattr(self.page, element.cid):
            self.add_component(element)
        if position is not None:
            self.switch_component(self.cid, element.cid, position=position)
        self.redraw()

    def handle_add_dragable(self, cid, position):
        self.switch_component(self.cid, cid, position=position)

    def get_valid_types(self, dotted=False):
        if dotted:
            return json.dumps(['.droppable_type_%s' % t.type for t in self.valid_types])
        return ' '.join(['droppable_type_%s' % t.type for t in self.valid_types])
