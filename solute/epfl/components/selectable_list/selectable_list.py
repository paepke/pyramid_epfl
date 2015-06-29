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



    js_parts = PaginatedListLayout.js_parts + ["selectable_list/selectable_list.js"]
    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:selectable_list/static', 'selectable_list.js')]

    compo_state = PaginatedListLayout.compo_state + ["search_text","scroll_pos"]

    search_text = None #: search text for custom search text handling

    scroll_pos = None #: Scrollbar position this is used to jump back to the last scroll pos after redraw

    def __init__(self,page,cid, data_interface=None, *args, **extra_params):
        """
        Selectable List is a MultiSelect Component, multiple values can be selected
        :param data_interface: data interface for child class needs id and text
        """
        super(SelectableList, self).__init__(page,cid,data_interface=data_interface, *args, **extra_params)

    def handle_select(self, cid):
        self.page.components[cid].selected = not self.page.components[cid].selected
        self.redraw()

    def handle_double_click(self, cid):
        # Overwrite me for doubleclick handling
        pass

    def get_selected(self):
        """
        :return: a list with selected compontents
        """
        return [compo for compo in self.components if compo.selected]

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        super(SelectableList, self).handle_set_row(row_offset, row_limit, row_data)
        if row_data is not None:
            self.search_text = row_data.get("search")
        self.update_children()
        self.redraw()

    def handle_scroll(self,scroll_pos):
        self.scroll_pos = scroll_pos
