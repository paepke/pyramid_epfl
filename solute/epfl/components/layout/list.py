# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class ListLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "layout/list.html"
    asset_spec = "solute.epfl.components:layout/static"

    css_name = ["bootstrap.min.css"]

    compo_state = ['links']
    compo_state.extend(epflcomponentbase.ComponentContainerBase.compo_state)

    links = []

    def __init__(self, node_list=[], links=[], **extra_params):
        super(ListLayout, self).__init__()


class PaginatedListLayout(ListLayout):
    template_name = "layout/paginated_list.html"
    js_parts = ['layout/paginated_list.js']