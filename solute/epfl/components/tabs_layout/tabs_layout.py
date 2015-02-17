from solute.epfl.core import epflcomponentbase


class TabsLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "tabs_layout/tabs_layout.html"
    
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["tabs_layout/tabs_layout.js"]
    
    asset_spec = "solute.epfl.components:tabs_layout/static"

    js_name = ["bootstrap.tab.js", "tabs_layout.js"]

    compo_state = ["active_tab_cid"]

    active_tab_cid = ""

    def handle_toggle_tab(self, selected_compo_cid):
        self.active_tab_cid = selected_compo_cid
        self.redraw()

    def del_component(self, compo_obj, slot=None):
        position = None
        if compo_obj.cid == self.active_tab_cid:
            position = self.components.index(compo_obj)
        super(TabsLayout, self).del_component(compo_obj, slot)
        if position > 0:
            self.handle_toggle_tab(self.components[position-1].cid)
            self.redraw()
