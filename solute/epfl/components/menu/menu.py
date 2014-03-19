# coding: utf-8

"""

"""

import types, copy

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Menu(epflcomponentbase.ComponentBase):

    template_name = "menu/menu.html"
    asset_spec = "solute.epfl.components:menu/static"

    js_name = ["menu.js"]

    css_name = ["menu.css"]

    compo_state = []

    compo_config = ["menu_def"]

    # menu config:

    menu_def = {'items':[]} # [{"label": "Dashboard", "route_name": "home"},
                            #  {"label": "Publikationen", "route_name": "publikationen",
                            #        "items": [{"label": u"Übersicht", "route_name": "publikationen"},
                            #                  {"label": "neue Publikationen", "route_name": "publikationen_formular"}
                            #                  ]
                            #   },
                            #   ...
                            #  ]


    def is_selected(self, item):

## todo        href = item.get("href")
##       if href:
##            if self.request.url.path == href:
##                return True

        return False

    def pre_render(self):
        super(Menu, self).pre_render()

        def filter_access(item):
            route_name = item.get("route_name")

            if not route_name:
                item["visible"] = True
            else:
                item["visible"] = True # todo user.has_page_access(__svc__.epfl.get_page(page_name))

            for subitem in item.get("items", []):
                filter_access(subitem)

        def add_class(item):

            child_is_selected = False
            for subitem in item.get("items", []):
                if not child_is_selected:
                    child_is_selected = add_class(subitem)
                else:
                    add_class(subitem)

            if self.is_selected(item) or child_is_selected:
                item["class"] = "active"
                return True
            else:
                item["class"] = ""
                return False

        filter_access(self.menu_def)
        add_class(self.menu_def)

