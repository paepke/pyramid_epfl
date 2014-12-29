from solute.epfl.core import epflcomponentbase
from solute.epfl.components.droppable.droppable import Droppable
from solute.epfl.components.dragable.dragable import Dragable

class FlipFlopDragable(Dragable):
    type = "flipflopdragable"

    def get_child_cid(self):
        self.components[0].get_component_id()


class FlipFlop(Droppable):

    compo_state = ["components_order"]

    compo_config = []
    
    components_order = []

    valid_types = [FlipFlopDragable]

    def init_struct(self):
        node_list = []

        for compo in self.node_list:
            new_container = FlipFlopDragable(node_list=[compo])
            node_list.append(new_container)

        return node_list

    def init_transaction(self):
        super(FlipFlop, self).init_transaction()
        if self.components_order:
            self.order_components()
        else:
            for compo in self.components:
                self.components_order.append(compo.get_child_cid())

    def get_components_order(self):
        return self.components_order

    def set_component_order(self,order):
        self.components_order = order

    def order_components(self,new_order=None):
        if(new_order):
            self.set_component_order(new_order)

        pos = 0

        for child_compo_cid in self.components_order:
            for compo in self.components:
                if child_compo_cid == compo.components[0].cid:
                    self.switch_component(self.cid,compo.cid,position=pos)
                    break

            pos += 1

    def handle_add_dragable(self, cid, position):
        super(FlipFlop,self).handle_add_dragable(cid,position)
        self.components_order = []
        for compo in self.components:
            self.components_order.append(compo.components[0].cid)
