# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase


class NavLayout(epflcomponentbase.ComponentBase):
    template_name = "layout/nav.html"
    asset_spec = "solute.epfl.components:layout/static"

    css_name = ["bootstrap.min.css"]

    compo_state = ['links', 'title']

    title = None
    links = []

    def __init__(self, title=None, links=[], **extra_params):
        super(NavLayout, self).__init__()