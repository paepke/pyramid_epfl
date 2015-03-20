# coding: utf-8

"""

"""

from solute.epfl.components import ListLayout


class PrettyListLayout(ListLayout):

    asset_spec = "solute.epfl.components:pretty_list_layout/static"
    theme_path = ListLayout.theme_path + ["pretty_list_layout/theme"]

    # : The max height of the list view. If the entries exceed the height, a scrollbar is displayed.
    height = None

    css_name = ListLayout.css_name + \
        [("solute.epfl.components:pretty_list_layout/static", "pretty_list_layout.css")]
