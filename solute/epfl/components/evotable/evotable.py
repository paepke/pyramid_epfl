from solute.epfl.core import epflcomponentbase

class Row(epflcomponentbase.ComponentTreeBase):
    template_name = "evotable/row.html"
    asset_spec = "solute.epfl.components:evotable/static"

class Cell(epflcomponentbase.ComponentTreeBase):
    template_name = "evotable/cell.html"
    asset_spec = "solute.epfl.components:evotable/static"

class TextValue(epflcomponentbase.ComponentBase):
    template_name = "evotable/textvalue.html"
    asset_spec = "solute.epfl.components:evotable/static"
    value = None
    component_state = ["value"]

class EvoTable(epflcomponentbase.ComponentTreeBase):
    template_name = "evotable/evotable.html"
    asset_spec = "solute.epfl.components:evotable/static"

    css_name = ["bootstrap.min.css"]
    js_name = []

    compo_state = ["table_data"]

    table_data = []

    def init_tree_struct(self):
        node_list = []

        for row in self.table_data:
            row_node_list = []
            node_list.append(Row(node_list=row_node_list))

            for cell in row:
                if type(cell) != int and type(cell) != str:
                    new_cell = Cell(node_list=[cell])
                    row_node_list.append(new_cell)
                else:
                    text_value = TextValue(value=cell)
                    new_cell = Cell(node_list=[text_value])
                    row_node_list.append(new_cell)

        return node_list

    def get_data(self):
        """
        overwrite me !!!

        """
        return []

    def reload(self):
        print "reload table"
        new_table_data = self.get_data()
        from pprint import pprint
        #pprint(new_table_data)
        pprint(self.components)

        for compo in self.components:
            self.del_component(compo)

        pprint(self.components)

        #for compo in self.components:
        #    self.del_component(compo)

        """
        for row_data in self.table_data:
            row = Row()


            for cell_data in row_data:
                if type(cell) != int and type(cell) != str:
                    new_cell = Cell(node_list=[cell])
                    row_node_list.append(new_cell)
                else:
                    text_value = TextValue(value=cell)
                    new_cell = Cell(node_list=[text_value])
                    row_node_list.append(new_cell)
        """

        self.redraw()

