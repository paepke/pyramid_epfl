from solute.epfl.core import epflcomponentbase

class TabsLayout(epflcomponentbase.ComponentContainerBase):
    template_name = "tabs_layout/tabs_layout.html"
    
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["tabs_layout/tabs_layout.js"]
    
    asset_spec = "solute.epfl.components:tabs_layout/static"

    js_name = ["tabs_layout.js"]

    compo_state = ["active_tab_cid"]

    active_tab_cid = ""

    def handle_toggle_tab(self, selected_compo_cid):
        self.active_tab_cid = selected_compo_cid
        self.add_js_response("$('#%s_tabmenuentry').tab('show');" % self.active_tab_cid)

    def del_component(self, cid, slot=None):
        position = None
        if cid.cid == self.active_tab_cid:
            position = self.components.index(cid)
        super(TabsLayout, self).del_component(cid, slot)
        if position > 0:
            self.handle_toggle_tab(self.components[position-1].cid)
            self.redraw()
