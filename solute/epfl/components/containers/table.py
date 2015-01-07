from solute.epfl.core import epflcomponentbase


class Row(epflcomponentbase.ComponentContainerBase):
    pass


class Cell(epflcomponentbase.ComponentContainerBase):
    pass


class TextValue(epflcomponentbase.ComponentBase):
    template_name = "containers/textvalue.html"
    asset_spec = "solute.epfl.components:containers/static"
    value = None
    compo_state = ["value"]


class TableContainer(epflcomponentbase.ComponentContainerBase):
    template_name = "containers/table.html"
    asset_spec = "solute.epfl.components:containers/static"

    css_name = ["bootstrap.min.css"]
    js_name = []

    compo_state = ["table_data"]

    table_data = []

    def init_struct(self):
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

