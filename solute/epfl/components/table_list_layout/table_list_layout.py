# * encoding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ListLayout


class TableLayoutRow(epflcomponentbase.ComponentContainerBase):
    """
    Only for internal use as child compo of TableListLayout

    """
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
    """

    A container component that renders the given data in a table

    The visual of a cell, for example is it a text or a progress or whatever,
    can be defined via a type tag in the data structure. For a easier handling use the static methods

    * HeadRow
    * HeadText
    * Row
    * Text
    * Progress
    * Icon
    * Compo
    * Badge
    * Edit
    * Popover

    for this.

    Example Data:

    .. code-block:: python

        data = []

        data.append(TableListLayout.HeadRow([TableListLayout.HeadText(u'Kategorie'),
                                             TableListLayout.HeadText('Live'),
                                             TableListLayout.HeadText('Relevanz'),
                                             TableListLayout.HeadText('FaktorRelevanz'),
                                             TableListLayout.HeadText('Erfassung Gesamt'),
                                             TableListLayout.HeadText('Datum'),
                                             TableListLayout.HeadText('User'),
                                             TableListLayout.HeadText('Aktion')]))

        for rowid in range(1, 1000):
            data.append(TableListLayout.Row(rowid, [TableListLayout.Text("Notebooks (2303)"),
                                                    TableListLayout.Progress(
                                                        [TableListLayout.ProgressPart("1.412", "33%", "success"),
                                                         TableListLayout.ProgressPart("70", "1.5%", "warning"),
                                                         TableListLayout.ProgressPart("2.852", "64%", "danger"),
                                                         TableListLayout.ProgressPart("2", "1.5%")]),
                                                    TableListLayout.Progress(
                                                        [TableListLayout.ProgressPart("1.412", "33%", "success"),
                                                         TableListLayout.ProgressPart("70", "1.5%", "warning"),
                                                         TableListLayout.ProgressPart("2.852", "64%", "danger"),
                                                         TableListLayout.ProgressPart("2", "1.5%")]),
                                                    TableListLayout.Text("153,1"),
                                                    TableListLayout.Text("364 Produkte"),
                                                    TableListLayout.Text("24.09.2014 13:37 Uhr"),
                                                    TableListLayout.Icon("user", "dab", "1"),
                                                    TableListLayout.Compo(ButtonSet())
                                                    ]))


    """

    theme_path = ['paginated_list_layout/theme', 'table_list_layout/theme']

    js_parts = ListLayout.js_parts[:]
    js_parts.extend(['paginated_list_layout/paginated_list_layout.js', 'table_list_layout/table_list_layout.js'])
    default_child_cls = TableLayoutRow

    show_pagination = True
    show_search = True

    #: False - You have to call update_children yourself, True - epfl call update_children automatically
    auto_update_children = False

    compo_state = ListLayout.compo_state[:]
    compo_state.extend(["orderby", "ordertype", "search", "height"])

    js_name = ["table_list_layout.js"]
    css_name = ["table_list_layout.css"]
    asset_spec = "solute.epfl.components:table_list_layout/static"


    orderby = ""
    ordertype = "asc"
    search = ""
    height = None
    data_interface = {'id': None, 'data': None}

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        self.row_offset, self.row_limit, self.row_data = row_offset, row_limit, row_data
        self.update_children()
        self.redraw()


    def handle_edit(self, entry_id, data):
        """
        Overwrite this for edit handling
        This is called when you click on an edit button
        """
        pass

    def handle_export_csv(self):
        """
        Overwrite this for csv handling
        This is called when you click on the csv button
        """
        pass

    @staticmethod
    def HeadRow(headings):
        headrow = {'id': 0, 'data': []}

        for head in headings:
            headrow['data'].append(head)

        return headrow

    @staticmethod
    def HeadText(text, sortable=False, currentSortedBy=False, direction='asc', width=None):
        head = {'data': text, "sortable": sortable, "currentSortedBy": currentSortedBy, "direction": direction,
                'type': 'head', "width": width}
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
    def Button(name, event_name, button_params=None, text=None, icon=None):
        button = {"type": 'button'}
        button['data'] = {"name": name, "handler": event_name}
        if text:
            button['data']['text'] = text
        if icon:
            button['data']['icon'] = icon
        if button_params:
            button['data']['button_params'] = button_params
        return button

    @staticmethod
    def Popover(text,popover_text):
        return {"text":text,"popover_text":popover_text,"type": "popover"}