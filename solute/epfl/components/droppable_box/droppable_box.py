# * encoding: utf-8

from solute.epfl.components import Box


class DroppableBox(Box):
    drop_position = None
    js_name = Box.js_name + [("solute.epfl.components:droppable_box/static", "droppable_box.js")]
    js_parts = Box.js_parts + ['droppable_box.js']
    

    def handle_drag_stop(self, position=None, cid=None, over_cid=None):
        if position is None:
            position = self.drop_position
            if cid in self.struct_dict and self.struct_dict.key_index(cid) < position:
                position -= 1
        if over_cid is not None and over_cid in self.struct_dict:
            position = self.struct_dict.key_index(over_cid)
            if cid in self.struct_dict and self.struct_dict.key_index(cid) < position:
                position -= 1
        self.switch_component(self.cid, cid, position=position)

    def handle_drop_accepts(self, cid=None):
        pass
