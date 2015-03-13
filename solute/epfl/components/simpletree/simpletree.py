# coding: utf-8

from solute.epfl.core import epflcomponentbase
from collections2 import OrderedDict as odict


class Simpletree(epflcomponentbase.ComponentBase):
    template_name = "simpletree/simpletree.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletree/simpletree.js"]

    asset_spec = "solute.epfl.components:simpletree/static"

    js_name = ["simpletree.js",("solute.epfl:static", "plugin/contextmenu.js")]

    css_name = ["simpletree.css"]

    compo_config = []
    compo_state = ["tree_data", "search_string", "open_leaf_0_ids", "open_leaf_1_ids", "all_filter", "filter_key",
                   "scroll_top", "selected_0_id", "selected_1_id", "selected_2_id"]

    tree_data = odict()

    open_leaf_0_ids = []
    open_leaf_1_ids = {}
    all_filter = []

    height = 400

    search_string = None
    filter_key = None

    scroll_top = 0
    selected_0_id = None
    selected_1_id = None
    selected_2_id = None

    # TREE DATA
    def reset_tree_data(self):
        self.tree_data = odict()

    def add_level_0(self, data):
        for entry in data:
            self.tree_data[entry['id']] = entry


    def add_level_1(self, data, parent_id):
        self.tree_data[parent_id]["children"] = odict()
        for entry in data:
            self.tree_data[parent_id]["children"][entry['id']] = entry

    def remove_level_1(self, parent_id):
        try:
            del self.tree_data[parent_id]["children"]
        except KeyError:
            pass


    def add_level_2(self, data, level_1_id, level_0_id):
        if not "children" in self.tree_data[level_0_id]:
            return

        if not level_1_id in self.tree_data[level_0_id]["children"]:
            return

        self.tree_data[level_0_id]["children"][level_1_id]["children"] = odict()
        for entry in data:
            self.tree_data[level_0_id]["children"][level_1_id]["children"][entry['id']] = entry

    def remove_level_2(self, level_1_id, level_0_id):
        try:
            del self.tree_data[level_0_id]["children"][level_1_id]["children"]
        except KeyError:
            pass


    def init_transaction(self):
        self.add_level_0(self.load_level_0())

    def load_level_0(self):
        return []

    def load_level_1(self, upper_leaf_id):
        return []

    def load_level_2(self, upper_leaf_id):
        return []

    def rebuild_tree_structure(self):
        self.reset_tree_data()

        self.add_level_0(self.load_level_0())

        for leafid in self.open_leaf_0_ids:
            if leafid in self.tree_data.keys():
                self.add_level_1(self.load_level_1(leafid), leafid)
            else:
                self.open_leaf_0_ids.remove(leafid)
        deprecated_leaf_1_ids = []
        for leaf_id, leaf_obj in self.open_leaf_1_ids.iteritems():
            if (leaf_obj["parent_id"] in self.tree_data.keys()) and ('children' in self.tree_data[leaf_obj['parent_id']]) and (leaf_id in self.tree_data[leaf_obj['parent_id']]['children'].keys()):
                self.add_level_2(self.load_level_2(leaf_id),
                                 leaf_id, leaf_obj["parent_id"])
            else:
                deprecated_leaf_1_ids.append(leaf_id)
        for leaf_id in deprecated_leaf_1_ids:
            del self.open_leaf_1_ids[leaf_id]

        self.redraw()

    def update_level_0(self, recursive=False):
        if recursive:
            self.rebuild_tree_structure()
            return
        level_0_data = self.load_level_0()
        new_tree_data = odict()
        for entry in level_0_data:
            if (entry["id"] in self.tree_data) and ("children" in self.tree_data[entry["id"]]):
                children = self.tree_data[entry["id"]]["children"]
                new_tree_data[entry["id"]] = entry
                new_tree_data[entry["id"]]["children"] = children
            else:
                new_tree_data[entry["id"]] = entry
        self.tree_data = new_tree_data
        self.redraw()

    def update_level_1(self, level_0_id, recursive=False): 
        level_1_data = self.load_level_1(level_0_id)
        new_level_1_data = odict()
        recursive_update_ids=[]
        for entry in level_1_data:
            if ("children" in self.tree_data[level_0_id]) and (entry["id"] in self.tree_data[level_0_id]["children"]) and ("children" in self.tree_data[level_0_id]["children"][entry["id"]]):
                if recursive:
                    recursive_update_ids.append(entry["id"])
                else:
                    children = self.tree_data[level_0_id]["children"][entry["id"]]["children"]
                    new_level_1_data[entry["id"]] = entry
                    new_level_1_data[entry["id"]]["children"] = children
            else:
                new_level_1_data[entry["id"]] = entry
        self.tree_data[level_0_id]["children"] = new_level_1_data
        
        for recursive_update_id in recursive_update_ids:
            self.update_level_2(level_0_id, recursive_update_id)
        
        self.redraw()
        
    def update_level_1_for_given_level_1_entry(self, level_1_id, recursive=False):
        level_0_id = None
        for entry_id, entry in self.tree_data.iteritems():
            if "children" in entry and (level_1_id in entry["children"].keys()):
                level_0_id = entry_id
                break
        if not level_0_id is None:
            self.update_level_1(level_0_id, recursive)

    def update_level_2(self, level_0_id, level_1_id):
        if not level_1_id in self.open_leaf_1_ids.keys():
            return
        level_2_data = self.load_level_2(level_1_id)
        new_level_2_data = odict()
        for entry in level_2_data:
            new_level_2_data[entry["id"]] = entry
        self.tree_data[level_0_id]["children"][level_1_id]["children"] = new_level_2_data
        self.redraw()

    def leaf_0_clicked(self, leafid):
        pass

    def handle_leaf_0_open(self, leafid, scroll_top):
        self.scroll_top = scroll_top
        leafid = int(leafid)

        self.add_level_1(self.load_level_1(leafid), leafid)
        if not leafid in self.open_leaf_0_ids:
            self.open_leaf_0_ids.append(leafid)

        self.leaf_0_clicked(leafid)

        self.redraw()


    def handle_leaf_0_close(self, leafid, scroll_top):
        self.scroll_top = scroll_top
        leafid = int(leafid)
        try:
            self.open_leaf_0_ids.remove(leafid)
        except ValueError:
            pass
        self.remove_level_1(leafid)

        self.redraw()


    def leaf_1_clicked(self, leafid, parent_id):
        pass

    def handle_leaf_1_open(self, leafid, parent_id, scroll_top):
        self.scroll_top = scroll_top

        self.add_level_2(self.load_level_2(leafid), leafid, parent_id)
        self.open_leaf_1_ids[leafid] = {"leafid": leafid, "parent_id": parent_id}

        self.leaf_1_clicked(leafid, parent_id)

        self.redraw()

    def handle_leaf_1_close(self, leafid, parent_id, scroll_top):
        self.scroll_top = scroll_top
        try:
            del self.open_leaf_1_ids[leafid]
        except KeyError:
            pass
        self.remove_level_2(leafid, parent_id)

        self.leaf_1_clicked(leafid, parent_id)

        self.redraw()

    def handle_leaf_2_clicked(self, leafid, scroll_top):
        self.scroll_top = scroll_top
        # Overwrite for click handling
        pass

    def handle_search(self, search_string, filter_key):
        self.search_string = search_string
        self.filter_key = filter_key
        self.rebuild_tree_structure()

    def handle_drop(self,
                    drag_leafid,drag_parent_leafid,drag_level_0_leafid,drag_tree_cid,
                    drop_leafid,drop_parent_leafid,drop_level_0_leafid,drop_tree_cid):
        pass




