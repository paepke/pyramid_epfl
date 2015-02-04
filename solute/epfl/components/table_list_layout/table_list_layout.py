# * encoding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ListLayout


class TableLayoutRow(epflcomponentbase.ComponentContainerBase):
    template_name = "table_list_layout/table_row.html"
    asset_spec = "solute.epfl.components:table_list_layout/static"

    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + ["current_compo"]

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
    # TODO: is there a better way to make use of paginated layout stuff? Inheriting from PaginatedListLayout?
    theme_path = ['paginated_list_layout/theme', 'table_list_layout/theme']

    js_parts = ListLayout.js_parts[:]
    js_parts.extend(['paginated_list_layout/paginated_list_layout.js', 'table_list_layout/table_list_layout.js'])
    default_child_cls = TableLayoutRow

    show_pagination = True
    show_search = True

    compo_state = ListLayout.compo_state[:]
    compo_state.extend(["orderby", "ordertype", "search", "height"])

    orderby = ""
    ordertype = "asc"
    search = ""
    height = None
    data_interface = {'id': None, 'data': None}


    def handle_edit(self, id, data):
        # Overwrite this for edit handling
        pass

    def handle_export_csv(self):
        # Overwrite this for csv handling
        pass

    @staticmethod
    def HeadRow(headings):
        headrow = {'id': 0, 'data': []}

        for head in headings:
            headrow['data'].append(head)

        return headrow

    @staticmethod
    def HeadText(text, sortable=False, currentSortedBy=False, direction='asc'):
        head = {'data': text, "sortable": sortable, "currentSortedBy": currentSortedBy, "direction": direction,
                'type': 'head'}
        return head

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

    @staticmethod
    def Edit(disabled=False):
        edit = {"type": "edit"}
        if disabled:
            edit["disabled"] = "disabled"
        return edit

    @staticmethod
    def Popover(text,popover_text):
        return {"text":text,"popover_text":popover_text,"type": "popover"}