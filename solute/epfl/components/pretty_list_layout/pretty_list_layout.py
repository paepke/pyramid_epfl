# coding: utf-8

"""

"""

from solute.epfl.components import ListLayout


class PrettyListLayout(ListLayout):
    
    theme_path = ListLayout.theme_path + ["pretty_list_layout/theme"]
