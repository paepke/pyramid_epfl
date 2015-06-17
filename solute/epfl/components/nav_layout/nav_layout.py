# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase

class NavLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "nav_layout/nav_layout.html"
    asset_spec = 'solute.epfl.components:nav_layout/static'

    css_name = epflcomponentbase.ComponentBase.css_name + ['nav_layout.css']

    compo_state = ['links', 'title', 'img']

    img = None
    title = None
    links = None

    def __init__(self, page, cid, title=None, links=[], **extra_params):
        super(NavLayout, self).__init__()
