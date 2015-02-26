# coding: utf-8

from solute.epfl.core import epflcomponentbase


class Simpletree(epflcomponentbase.ComponentBase):
    template_name = "simpletree/simpletree.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletree/simpletree.js"]

    asset_spec = "solute.epfl.components:simpletree/static"

    js_name = ["simpletree.js"]

    css_name = ["simpletree.css"]

    compo_config = []
    compo_state = ["tree_data", "search", "open_leaf_0_ids", "open_leaf_1_ids", "all_filter", "filter"]

    tree_data = []
    open_leaf_0_ids = []
    open_leaf_1_ids = []
    all_filter = []

    height = 400

    search = None
    filter = None

    def init_transaction(self):
        self.tree_data = self.load_level_0()

    def load_level_0(self, search=None, filter=None):
        return []

    def load_level_1(self, upper_leaf_id, search=None, filter=None):
        return []

    def load_level_2(self, upper_leaf_id, search=None, filter=None):
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

    def handle_search(self, search, filter):
        self.search = search
        self.filter = filter

        self.rebuild_tree_structure(search)

    def rebuild_tree_structure(self, search=None, filter=None):
        self.tree_data = self.load_level_0(search,filter)

        for id in self.open_leaf_0_ids:
            self.add_leaf_0_data(self.load_level_1(id, search,filter), id)

        for id in self.open_leaf_1_ids:
            self.add_leaf_1_data(self.load_level_2(id, search,filter), id)

        self.redraw()

    def handle_drop(self, drag_leafid, drag_parent_cid, drop_leafid, drop_parent_cid):
        pass




