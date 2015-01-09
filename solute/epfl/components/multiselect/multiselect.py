from solute.epfl.core import epflcomponentbase
import json


class MultiSelect(epflcomponentbase.ComponentContainerBase):
    """
    
    A container component that renders the components as a multi-select list
    
    The nested components can be of arbitrary type, but they must have the epfl id attribute
    set in their outmost html element
    
    """
    
    template_name = "multiselect/multiselect.html"
    js_parts = "multiselect/multiselect.js"
    asset_spec = "solute.epfl.components:multiselect/static"

    css_name = ["multiselect.css", "bootstrap.min.css",
                "css/font-awesome/css/font-awesome.min.css"]
    js_name = ["multiselect.js"]

    compo_config = []
    compo_config = epflcomponentbase.ComponentContainerBase.compo_config[:]
    compo_config.append("show_search")
    compo_config.append("grouped")
    
    compo_state = epflcomponentbase.ComponentContainerBase.compo_state[:]
    compo_state.append("selected_child_cids")
    compo_state.append("hidden_child_cids")
    compo_state.append("scroll_position")
    compo_state.append("search_string")
    
    selected_child_cids = set()
    hidden_child_cids = set()
    scroll_position = 0
    show_search = False
    search_string = ""
    
    grouped = False
    
    def handle_selected(self, child_cid):
        if not child_cid in self.selected_child_cids:
            self.selected_child_cids.add(child_cid)
        self.redraw()
        
    def handle_unselected(self, child_cid):
        try:
            self.selected_child_cids.remove(child_cid)
        except KeyError:
            pass
        self.redraw()
        
    def handle_scrolled(self, scroll_position):
        self.scroll_position = scroll_position
    
    def _handle_search_simple(self):
        for compo in self.components:
            if not self.search_string in compo.value.lower():
                self.hidden_child_cids.add(compo.cid)
                # this component is also not selected anymore
                try:
                    self.selected_child_cids.remove(compo.cid)
                except KeyError:
                    pass
    
    def _handle_search_grouped(self):
        number_of_matched_entries_for_group = 0
        current_group_cid = None
        current_group_matched = False
        for compo in self.components:
            if hasattr(compo, 'multiselect_group'):
                if (not current_group_cid is None) and (current_group_matched == False) and (number_of_matched_entries_for_group == 0):
                    self.hidden_child_cids.add(current_group_cid)
                if not self.search_string in compo.value.lower():
                    current_group_matched = False
                else:
                    current_group_matched = True
                current_group_cid = compo.cid
                number_of_matched_entries_for_group = 0
            else:
                if (current_group_matched == True):
                    # if the group matches, we don't hide this group member
                    number_of_matched_entries_for_group += 1
                    continue
                if not self.search_string in compo.value.lower():
                    self.hidden_child_cids.add(compo.cid)
                    # this component is also not selected anymore
                    try:
                        self.selected_child_cids.remove(compo.cid)
                    except KeyError:
                        pass
                else:
                    number_of_matched_entries_for_group += 1
        # check for the last group
        if (not current_group_cid is None) and (current_group_matched == False) and (number_of_matched_entries_for_group == 0):
            self.hidden_child_cids.add(current_group_cid)
                    
    
    def handle_search(self, search_string):
        self.search_string = search_string.strip().lower()
        self.hidden_child_cids.clear()
        if self.grouped == False:
            self._handle_search_simple()
        else:
            self._handle_search_grouped()
        self.redraw()
    
    
class MultiSelectTransfer(epflcomponentbase.ComponentBase):
    """
    
    Provides functionality to move items from one multi select to another
    
    
    """
    
    template_name = "multiselect/multiselecttransfer.html"
    js_parts = "multiselect/multiselecttransfer.js"
    asset_spec = "solute.epfl.components:multiselect/static"

    css_name = ["bootstrap.min.css",
                "css/font-awesome/css/font-awesome.min.css"]
    js_name = ["multiselecttransfer.js"]
    source_multi_select_cid = None
    target_multi_select_cid = None
    
        
    def handle_transfer(self):
        source_multiselect = self.page.components[self.source_multi_select_cid]
        target_multiselect = self.page.components[self.target_multi_select_cid]
        for cid in source_multiselect.selected_child_cids:
            target_multiselect.switch_component(target_multiselect.cid, cid)
            target_multiselect.selected_child_cids.add(cid)
        source_multiselect.selected_child_cids.clear()
        source_multiselect.redraw()
        target_multiselect.redraw()