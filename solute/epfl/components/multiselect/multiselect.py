from solute.epfl.core import epflcomponentbase
import json


class MultiSelectEntry(epflcomponentbase.ComponentBase):
    template_name = "multiselect/multiselect_entry.html"
    asset_spec = "solute.epfl.components:multiselect/static"


class MultiSelect(epflcomponentbase.ComponentContainerBase):

    """

    A container component that renders the components as a multi-select list

    The nested components can be of arbitrary type, but they must have the epfl id attribute
    set in their outmost html element

    """

    template_name = "multiselect/multiselect.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["multiselect/multiselect.js"]
    asset_spec = "solute.epfl.components:multiselect/static"

    css_name = ["multiselect.css", "bootstrap.min.css",
                "css/font-awesome/css/font-awesome.min.css"]
    js_name = ["multiselect.js"]

    compo_config = epflcomponentbase.ComponentContainerBase.compo_config + \
        ["show_search", "grouped"]

    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + \
        ["selected_child_cids", "hidden_child_cids", "selected_child_ids", "scroll_position",
            "search_string", "default_out_multiselect_transfer_cid"]

    default_child_cls = MultiSelectEntry
    selected_child_cids = set()  #: A list of child cids that are currently selected.
    
    #: smart components may re-generate cids for its child components. In this case, this list
    #: can be used to remember the selected components by its id. It will be automatically moved into cids of the :attr:`selected_child_cids`.
    selected_child_ids = set()
    
    #: A list of child cids that should be hidden (e.g. for only displaying search results).
    hidden_child_cids = set()
    
    scroll_position = 0  #: Used to save the scroll position of the list in the transaction.
    show_search = False  #: If true, a search bar and search functionality is provided.
    search_string = ""  #: Used to save the last search string in the transaction
    
    #: Set the cid of a :class:`solute.epfl.components.multiselect.multiselect.MultiSelectTransfer` object which is used to automatically
    #: transfer objects from this list to another one based on double-clicks.
    default_out_multiselect_transfer_cid = None

    grouped = False  #: Set to true if list contains grouped entries.

    def handle_selected(self, child_cid):
        if not child_cid in self.selected_child_cids:
            self.selected_child_cids.add(child_cid)
        self.redraw()

    def handle_unselected(self, child_cid):
        self.selected_child_cids.discard(child_cid)
        self.redraw()

    def handle_double_click(self, child_cid):
        if not self.default_out_multiselect_transfer_cid is None:
            transfer = self.page.components[self.default_out_multiselect_transfer_cid]
            transfer.transfer_single_element(child_cid)
        self.redraw()

    def handle_scrolled(self, scroll_position):
        self.scroll_position = scroll_position

    def _handle_search_simple(self):
        searchstring = self.search_string.lower()
        for compo in self.components:
            try:
                if not searchstring in compo.data["value"].lower():
                    self.hidden_child_cids.add(compo.cid)
                    # this component is also not selected anymore
                    self.selected_child_cids.discard(compo.cid)
            except KeyError:
                pass

    def _handle_search_grouped(self):
        number_of_matched_entries_for_group = 0
        current_group_cid = None
        current_group_matched = False
        searchstring = self.search_string.lower()
        for compo in self.components:
            if "multiselect_group" in compo.data:
                if (not current_group_cid is None) and (current_group_matched == False) and (number_of_matched_entries_for_group == 0):
                    self.hidden_child_cids.add(current_group_cid)
                try:
                    if not searchstring in compo.data["value"].lower():
                        current_group_matched = False
                    else:
                        current_group_matched = True
                except KeyError:
                    current_group_matched = False

                current_group_cid = compo.cid
                number_of_matched_entries_for_group = 0
            else:
                if (current_group_matched == True):
                    # if the group matches, we don't hide this group member
                    number_of_matched_entries_for_group += 1
                    continue
                try:
                    if not searchstring in compo.data["value"].lower():
                        self.hidden_child_cids.add(compo.cid)
                        # this component is also not selected anymore
                        self.selected_child_cids.discard(compo.cid)
                    else:
                        number_of_matched_entries_for_group += 1
                except KeyError as e:
                    pass
        # check for the last group
        if (not current_group_cid is None) and (current_group_matched == False) and (number_of_matched_entries_for_group == 0):
            self.hidden_child_cids.add(current_group_cid)

    def handle_search(self, search_string):
        self.search_string = search_string.strip()
        self.hidden_child_cids.clear()
        if self.grouped == False:
            self._handle_search_simple()
        else:
            self._handle_search_grouped()
        self.redraw()

    def update_children(self, force=False):
        """
        Overwrite :meth:`solute.epfl.core.epflcomponentbase.ComponentContainerBase.update_children` to check if :attr:`selected_child_cids` is properly filled.
        Smart components may re-generate cids of its child components, and thus cannot use
        :attr:`selected_child_cids` to indicate selected components. Instead, they use :attr:`selected_child_ids`
        to indicate selected components, since the id of a components does not change.
        In this method, we know that all components have been initialized and for all ids in 
        :attr:`selected_child_ids`, the corresponding component cid can be placed in :attr:`selected_child_cids`.
        """
        result = epflcomponentbase.ComponentContainerBase.update_children(self, force=force)
        if (len(self.selected_child_ids) > 0):
            for compo in self.components:
                if compo.id in self.selected_child_ids:
                    self.selected_child_cids.add(compo.cid)
            self.selected_child_ids.clear()
        return result


class MultiSelectTransfer(epflcomponentbase.ComponentBase):

    """
    Provides functionality to move items from one multi select to another.


    """

    template_name = "multiselect/multiselecttransfer.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts[:]
    js_parts.append("multiselect/multiselecttransfer.js")
    asset_spec = "solute.epfl.components:multiselect/static"

    css_name = ["bootstrap.min.css",
                "css/font-awesome/css/font-awesome.min.css"]
    js_name = ["multiselecttransfer.js"]
    #: The cid of the source :class:`solute.epfl.components.multiselect.multiselect.MultiSelect` component
    source_multi_select_cid = None
    #: The cid of the target :class:`solute.epfl.components.multiselect.multiselect.MultiSelect` component
    target_multi_select_cid = None

    def handle_transfer(self):
        """
        Called when transfer button is clicked.
        Overwrite this method if source or target component is a smart component!
        """

        source_multiselect = self.page.components[self.source_multi_select_cid]
        target_multiselect = self.page.components[self.target_multi_select_cid]
        if source_multiselect.is_smart() or target_multiselect.is_smart():
            # do nothing, source/target component is smart. This method has to be overwritten.
            return
        for cid in source_multiselect.selected_child_cids:
            source_multiselect.send(self.page.components[cid].id)
            target_multiselect.switch_component(target_multiselect.cid, cid)
            target_multiselect.selected_child_cids.add(cid)
        source_multiselect.selected_child_cids.clear()
        source_multiselect.redraw()
        target_multiselect.redraw()

    def transfer_single_element(self, cid):
        """
        Can be used to transfer a simple element (e.g. to directly handle double-clicks on multiselects).
        Overwrite this method if source or target component is a smart component!
        """

        source_multiselect = self.page.components[self.source_multi_select_cid]
        target_multiselect = self.page.components[self.target_multi_select_cid]
        if source_multiselect.is_smart() or target_multiselect.is_smart():
            # do nothing, source/target component is smart. This method has to be overwritten.
            return

        source_multiselect.send(self.page.components[cid].id)
        target_multiselect.switch_component(target_multiselect.cid, cid)
        target_multiselect.selected_child_cids.add(cid)
        source_multiselect.selected_child_cids.discard(cid)
        source_multiselect.redraw()
        target_multiselect.redraw()
