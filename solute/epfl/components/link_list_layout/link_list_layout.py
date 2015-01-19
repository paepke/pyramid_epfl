# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase
from solute.epfl.components import PaginatedListLayout

class LinkListLayout(PaginatedListLayout):
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'text': None,
                      'url': None}
    
    theme_path = PaginatedListLayout.theme_path + ['link_list_layout/theme']
        
    js_parts = PaginatedListLayout.js_parts + ['link_list_layout/link_list_layout.js']

    compo_state = PaginatedListLayout.compo_state + ['links']
    
    links = []

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        for i, link in enumerate(self.links):
            link['id'] = i
        return self.links




