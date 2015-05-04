# coding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout


class SelectableList(PaginatedListLayout):
    """
    Selectable List is a MultiSelect Component, multiple values can be selected
    """
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'text': None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['selectable_list/theme']}

    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:selectable_list/static', 'selectable_list.js')]

    compo_state = PaginatedListLayout.compo_state + ['selected_cids']

    selected_cids = []

    def handle_select(self, cid):
        if cid in self.selected_cids:
            self.selected_cids.remove(cid)
        else:
            self.selected_cids.append(cid)
        self.redraw()

    def get_selected(self):
        """
        :return: a list with the selected cids and their data (id and text)
        """
        selected = []
        for cid in self.selected_cids:
            selected.append({"cid": cid, "id": self.page.components[cid].id, "text": self.page.components[cid].text})
        return selected
