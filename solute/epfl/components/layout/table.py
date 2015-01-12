from solute.epfl.core import epflcomponentbase
from solute.epfl.components.layout.list import ListLayout

class TableLayoutRow(epflcomponentbase.ComponentContainerBase):
    template_name = "layout/TableRow.html"
    asset_spec = "solute.epfl.components:layout/static"

    def init_struct(self):
        super(TableLayoutRow,self).init_struct()
        node_list = []
        for data in self.data:
            if data["type"] == "component":
                node_list.append(data["data"])

        self.current_compo = 0
        return node_list

    def setup_component(self):
        super(TableLayoutRow,self).setup_component()
        for compo in self.components:
            compo.row_data = self.data

    def get_next_component(self):
        compo = self.components[self.current_compo]
        self.current_compo += 1
        return compo



class TableListLayout(ListLayout):
    theme_path = [ 'layout/list/paginated', 'layout/list/table']
    js_parts = ['layout/list/paginated.js','layout/list/table.js',]
    default_child_cls = TableLayoutRow

    compo_state = ["orderby","ordertype","search"]


    orderby = ""
    ordertype = "asc"
    search = ""
