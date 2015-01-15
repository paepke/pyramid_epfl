from solute.epfl.core import epflcomponentbase
from solute.epfl.components.layout.list import ListLayout


class TableLayoutRow(epflcomponentbase.ComponentContainerBase):
    template_name = "layout/TableRow.html"
    asset_spec = "solute.epfl.components:layout/static"
    compo_state = ["current_compo"]

    current_compo = 0

    def init_struct(self):
        super(TableLayoutRow, self).init_struct()
        node_list = []
        for data in self.data:
            if data["type"] == "component":
                node_list.append(data["data"])

        self.current_compo = 0
        return node_list

    def setup_component(self):
        super(TableLayoutRow, self).setup_component()

        for compo in self.components:
            compo.row_data = self.data
        self.current_compo = 0

    def get_next_component(self):
        compo = self.components[self.current_compo]
        self.current_compo += 1
        return compo


class TableListLayout(ListLayout):
    theme_path = ['layout/list/paginated', 'layout/list/table']
    js_parts = ['layout/list/paginated.js', 'layout/list/table.js', ]
    default_child_cls = TableLayoutRow

    show_pagination = True
    show_search = True

    compo_state = ["orderby", "ordertype", "search","height"]

    orderby = ""
    ordertype = "asc"
    search = ""
    height = None

    @staticmethod
    def HeadRow(headings):
        headrow = {'id': 0, 'data': []}

        for head in headings:
            headrow['data'].append({'data': head, 'type': 'head'})

        return headrow

    @staticmethod
    def Row(rowid, fields):
        row = {'id': rowid, 'data': []}

        for field in fields:
            row['data'].append(field)

        return row

    @staticmethod
    def Text(text):
        return {"data": text, "type": "text"}


    @staticmethod
    def Progress(parts):
        return {"data": parts, 'type': 'progress'}


    @staticmethod
    def ProgressPart(text, width, color=None):
        part = {'text': text, 'width': width}
        if color:
            part['color'] = color
        return part

    @staticmethod
    def Icon(icon, text=None, size=None, color=None):
        icon = {"icon": icon, 'type': 'icon'}
        if text:
            icon['text'] = text
        if size:
            icon['size'] = size
        if color:
            icon['color'] = color
        return icon

    @staticmethod
    def Compo(compo):
        return {"data": compo, 'type': 'component'}

    @staticmethod
    def Badge(badgetext, text=None, color=None):
        badge = {"badgetext": badgetext, "type": "badge"}
        if text:
            badge['text'] = text
        if color:
            badge['color'] = color
        return badge
