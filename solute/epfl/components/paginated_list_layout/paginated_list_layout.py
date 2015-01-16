# coding: utf-8

"""

"""

from solute.epfl.components import PrettyListLayout

class PaginatedListLayout(PrettyListLayout):
    show_pagination = True
    show_search = True
    
    theme_path = PrettyListLayout.theme_path[:]
    theme_path.append('paginated_list_layout/theme')

    js_parts = ['paginated_list_layout/paginated_list_layout.js']

