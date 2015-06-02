# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout


class SelectableEntry(epflcomponentbase.ComponentBase):
    """
    Internal use only
    """
    compo_state = PaginatedListLayout.compo_state + ['selected']
    selected = False

class SelectableList(PaginatedListLayout):
    """
    Selectable List is a MultiSelect Component, multiple values can be selected
    """
    default_child_cls = SelectableEntry
    data_interface = {'id': None,
                      'text': None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['selectable_list/theme']}

    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:selectable_list/static', 'selectable_list.js')]

    compo_state = PaginatedListLayout.compo_state + ["search_text"]

    search_text = None

    def __init__(self,page,cid, data_interface=None, *args, **extra_params):
        """
        Selectable List is a MultiSelect Component, multiple values can be selected
        :param data_interface: data interface for child class needs id and text
        """
        super(SelectableList, self).__init__(page,cid,data_interface=data_interface, *args, **extra_params)

    def handle_select(self, cid):
        self.page.components[cid].selected = not self.page.components[cid].selected
        self.redraw()

    def get_selected(self):
        """
        :return: a list with selected compontents
        """
        return [compo for compo in self.components if compo.selected]

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        if row_data is not None:
            self.search_text = row_data.get("search")
        self.update_children()
        self.redraw()
