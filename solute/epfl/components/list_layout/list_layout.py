# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class ListLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "list_layout/list_layout.html"

    theme_path_default = 'list_layout/default_theme'
    theme_path = []

    def __init__(self, node_list=[], links=[], **extra_params):
        super(ListLayout, self).__init__()

