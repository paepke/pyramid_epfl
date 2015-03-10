# coding: utf-8

from solute.epfl.core import epflcomponentbase


class Simpletree(epflcomponentbase.ComponentBase):
    template_name = "simpletree/simpletree.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletree/simpletree.js"]

    asset_spec = "solute.epfl.components:simpletree/static"

    js_name = ["simpletree.js"]

    css_name = ["simpletree.css"]

    compo_config = []
    compo_state = ["tree_data", "search_string", "open_leaf_0_ids", "open_leaf_1_ids", "all_filter", "filter_key"]

    tree_data = []
    open_leaf_0_ids = []
    open_leaf_1_ids = []
    all_filter = []

    height = 400

    search_string = None
    filter_key = None

    def init_transaction(self):
        self.tree_data = self.load_level_0()

    def load_level_0(self, search_string=None, filter_key=None):
        return []

    def load_level_1(self, upper_leaf_id, search_string=None, filter_key=None):
        return []

    def load_level_2(self, upper_leaf_id, search_string=None, filter_key=None):
        return []

    def handle_leaf_0_clicked(self, leafid):
        leafid = int(leafid)

        if leafid in self.open_leaf_0_ids:
            # close
            self.open_leaf_0_ids.remove(leafid)
            self.remove_leaf_0_data(leafid)
        else:
            # open
            self.add_leaf_0_data(self.load_level_1(leafid), leafid)
            self.open_leaf_0_ids.append(leafid)

        self.redraw()

    def add_leaf_0_data(self, leafdata, leafid):

        newData = []
        for entry in self.tree_data:
            if entry["id"] == leafid:
                entry["children"] = leafdata
            newData.append(entry)

        self.tree_data = newData

    def remove_leaf_0_data(self, leafid):
        newData = []
        for entry in self.tree_data:
            if entry["id"] == leafid:
                entry.pop("children", None)
            newData.append(entry)

        self.tree_data = newData

    def handle_leaf_1_clicked(self, leafid):

        if leafid in self.open_leaf_1_ids:
            # close
            self.open_leaf_1_ids.remove(leafid)
            self.remove_leaf_1_data(leafid)
        else:
            # open
            self.add_leaf_1_data(self.load_level_2(leafid), leafid)
            self.open_leaf_1_ids.append(leafid)

        self.redraw()

    def handle_leaf_2_clicked(self, leafid):
        # Overwrite for click handling
        pass

    def add_leaf_1_data(self, leafdata, leafid):
        new_data = []

        for entry in self.tree_data:
            if "children" in entry:
                new_children = []
                for child in entry["children"]:
                    if child["id"] == leafid:
                        child["children"] = leafdata
                    new_children.append(child)
                entry["children"] = new_children
            new_data.append(entry)

        self.tree_data = new_data

    def remove_leaf_1_data(self, leafid):
        new_data = []

        for entry in self.tree_data:
            if "children" in entry:
                new_children = []
                for child in entry["children"]:
                    if child["id"] == leafid:
                        child.pop("children", None)
                    new_children.append(child)
                entry["children"] = new_children
            new_data.append(entry)

        self.tree_data = new_data

    def handle_search(self, search_string, filter_key):
        self.search_string = search_string
        self.filter_key = filter_key

        self.rebuild_tree_structure()

    def rebuild_tree_structure(self):
        search_string = self.search_string
        filter_key = self.filter_key
        self.tree_data = self.load_level_0(search_string, filter_key)

        for leafid in self.open_leaf_0_ids:
            self.add_leaf_0_data(self.load_level_1(leafid, search_string, filter_key), leafid)

        for leafid in self.open_leaf_1_ids:
            self.add_leaf_1_data(self.load_level_2(leafid, search_string, filter_key), leafid)

        self.redraw()

    def handle_drop(self, drag_leafid, drag_parent_cid, drop_leafid, drop_parent_cid):
        pass




