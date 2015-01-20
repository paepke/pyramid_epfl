# * encoding: utf-8

from pyramid.view import view_config
from solute import epfl
from pyramid import security

from .first_step import FirstStepRoot

from solute.epfl.components import Box
from solute.epfl.components import DragBox
from solute.epfl.components import cfButton


class DropBox(Box):
    drop_position = None
    js_name = Box.js_name + [('epfl_pyramid_barebone:static', 'drop.js')]
    js_parts = Box.js_parts + ['epfl_pyramid_barebone:templates/drop.js']

    def handle_drop_update_position(self, position):
        position = int(position)
        if position == -1:
            position = None
        self.drop_position = position

    def handle_drag_stop(self, position=None, cid=None):
        if position is None:
            position = self.drop_position
            if cid in self.struct_dict and self.struct_dict.key_index(cid) < position:
                position -= 1
        self.switch_component(self.cid, cid, position=position)

    def handle_drop_accepts(self, cid, position=None):
        self.add_drop_zone(cid, position)

    def add_drop_zone(self, cid, position):
        import json
        cids = [c.cid for c in self.components if c.cid != cid]

        if position is None and cids:
            before = False
            position = cids[-1]
        elif cids:
            before = True
            position = cids[position]
        else:
            before = False
            position = False
        self.add_js_response('epfl.add_drop_zone("%(cid)s", %(pos)s);' % {'cid': self.cid,
                                                                          'pos': json.dumps([position,
                                                                                             before])})


class FourthStepRoot(FirstStepRoot):
    node_list = FirstStepRoot.node_list + [DropBox(slot='west',
                                                   node_list=[DragBox(title=1),
                                                              DragBox(title=2),
                                                              DragBox(title=3),
                                                              DragBox(title=4),
                                                              DragBox(title=5), ]),
                                           DropBox(cid='second_drop')]

    def init_struct(self):
        pass


@view_config(route_name='FourthStep')
class FourthStepPage(epfl.Page):
    root_node = FourthStepRoot()
