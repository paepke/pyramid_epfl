
from solute.epfl.core import epflcomponentbase

class Row(object):
    cells = []

class Cell(object):
    value = None

class EvoTable(epflcomponentbase.ComponentTreeBase):

    template_name = "evotable/evotable.html"
    asset_spec = "solute.epfl.components:evotable/static"

    css_name = ["bootstrap.min.css"]
    js_name = []

    compo_state = []

    rows = []

    def init_tree_struct(self):
        self.rows = []

        for i in range(0,4):
            row = Row()
            for j in range(0,4):
                cell = Cell()
                cell.value = str(i) + " " + str(j)
                row.cells.append(cell)
            self.rows.append(row)

        return []

    def add_row(self,cells):
        pass
