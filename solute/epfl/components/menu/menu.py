# coding: utf-8

"""

"""

import types, copy

from pyramid import security

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

    menu_def = {'items':[]} # [{"label": "Dashboard", "route": "home"},
                            #  {"label": "Publikationen", "route": "publikationen",
                            #        "items": [{"label": u"Übersicht", "route": "publikationen"},
                            #                  {"label": "neue Publikationen", "route": "publikationen_formular", "route_params": ("new",)}
                            #                  ]
                            #   },
                            #   ...
                            #  ]


    def is_selected(self, item):
        return self.request.matched_route.name == item.get("route")


    def pre_render(self):
        super(Menu, self).pre_render()


        def filter_access(item):
            route_name = item.get("route")

            if not route_name:
                item["visible"] = True
            else:
                item["visible"] = epflutil.has_permission_for_route(self.request, route_name, "access")

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

    def get_href(self, menu_item):

        if menu_item["route"]:
            return self.request.route_path(menu_item["route"], **menu_item.get("route_params", {}))


        return "#"

