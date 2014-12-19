
from solute.epfl.core import epflcomponentbase

class Tab(epflcomponentbase.ComponentTreeBase):
    
    template_name = "tab/tab.html"
    asset_spec = "solute.epfl.components:tab/static"

    css_name = ["bootstrap.min.css"]
    js_name = ["bootstrap.tab.js", "tab.js"]


    compo_state = [ "active_tab_cid"]
    
    active_tab_cid = ""
    
    def handle_toggleTab(self, selected_compo_cid):
        #self.page.components[self.active_tab_cid].set_hidden()
        #self.page.components[self.active_tab_cid].redraw()
        #self.page.components[selected_compo_cid].redraw()
        self.active_tab_cid = selected_compo_cid
        