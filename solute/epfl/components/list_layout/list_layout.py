# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class ListLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "list_layout/list_layout.html"

    theme_path_default = 'list_layout/default_theme'
    theme_path = []

    def __init__(self, page, cid, **extra_params):
        """Simple list style container component.
        """
        super(ListLayout, self).__init__()

