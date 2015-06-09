# * encoding: utf-8

from __future__ import unicode_literals

from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout


class CategorySelectList(PaginatedListLayout):
    """
    CategorySelectList is a typeahead input containing a list of entries and sub entries
    """
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'value': None,
                      'entries':None}

    theme_path = {'default': PaginatedListLayout.theme_path,
                  'row': ['category_select_list/theme'],
                  'before': ['category_select_list/theme'],
                  'after': ['category_select_list/theme'],}



    js_name = PaginatedListLayout.js_name + [('solute.epfl.components:category_select_list/static', 'category_select_list.js')]
    css_name = PaginatedListLayout.js_name + [('solute.epfl.components:category_select_list/static', 'category_select_list.css')]

    compo_state = PaginatedListLayout.compo_state + ["selected_text"]

    selected_text = None #: Current Selected text

    new_style_compo = True
    js_parts = []
    compo_js_name = 'CategorySelectList'
    compo_js_params = ['show_search','show_pagination','row_limit','row_offset','selected_text']
    compo_js_extras = ['handle_click','handle_keyup']


    # auto_update_children = True
    show_search = True
    show_pagination = False

    def __init__(self,page,cid, data_interface=None, *args, **extra_params):
        """
        CategorySelectList is a typeahead input containing a list of entries and sub entries
        :param data_interface: data interface for child class needs id and text and entries
        """
        super(CategorySelectList, self).__init__(page,cid,data_interface=data_interface, *args, **extra_params)

    def handle_set_selection(self, selection_id, selection_value, selection_group_id, selection_group_value):
        """
        Don't overwrite this use the post_event_handler system
        """
        self.value = selection_id
        self.selected_text = selection_value
