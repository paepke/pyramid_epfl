from solute.epfl.core import epflcomponentbase


class TabsLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "tabs_layout/tabs_layout.html"
    js_parts = "tabs_layout/tabs_layout.js"
    asset_spec = "solute.epfl.components:tabs_layout/static"

    js_name = ["js/jquery-1.8.2.min.js", "bootstrap.tab.js", "tabs_layout.js"]

    compo_state = ["active_tab_cid"]

    active_tab_cid = ""

    def handle_toggle_tab(self, selected_compo_cid):
        self.active_tab_cid = selected_compo_cid
