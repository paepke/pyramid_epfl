from solute.epfl.core import epflcomponentbase
from solute.epfl.components.dragable.dragable import Dragable
import json


class Droppable(epflcomponentbase.ComponentContainerBase):
    template_name = "droppable/droppable.html"
    asset_spec = "solute.epfl.components:droppable/static"

    css_name = ["droppable.css", "bootstrap.min.css", "css/font-awesome/css/font-awesome.min.css"]
    js_name = ["droppable.js"]

    compo_config = ["valid_types"]
    compo_state = ["elements", "is_collapsed", "title"]

    valid_types = [Dragable]
    elements = []
    collapsable=False
    title_renamable = False
    is_collapsed=False
    title=None
    
    def __init__(self, title=None, collapsable=False, title_renamable=False, **extra_params):
        super(Droppable, self).__init__()
        
        
        
    def init_transaction(self):
        super(Droppable, self).init_transaction()
        if (self.collapsable == True) and (self.title is None):
            raise RuntimeError("Title must be set for collapsable droppables!")

    def add_dragable_element(self, element, position=None):
        if not hasattr(element, 'cid') or not hasattr(self.page, element.cid):
            self.add_component(element)
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
