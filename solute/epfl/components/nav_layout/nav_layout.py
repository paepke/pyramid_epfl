# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase

class NavLayout(epflcomponentbase.ComponentBase):
    template_name = "nav_layout/nav_layout.html"

    compo_state = ['links', 'title']

    title = None
    links = None

    def __init__(self, title=None, links=[], **extra_params):
        super(NavLayout, self).__init__()
