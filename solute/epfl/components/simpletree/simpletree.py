# coding: utf-8

from solute.epfl.core import epflcomponentbase
from collections2 import OrderedDict as odict

class Simpletree(epflcomponentbase.ComponentBase):
    template_name = "simpletree/simpletree.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletree/simpletree.js"]

    asset_spec = "solute.epfl.components:simpletree/static"

    js_name = ["simpletree.js"]

    css_name = ["simpletree.css"]

    compo_config = []
    compo_state = ["tree_data", "search_string", "open_leaf_0_ids", "open_leaf_1_ids", "all_filter", "filter_key",
                   "scroll_top","selected_0_id","selected_1_id","selected_2_id"]

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
        del self.tree_data[parent_id]["children"]


    def add_level_2(self, data, level_1_id, level_0_id):
        if not "children" in self.tree_data[level_0_id]:
            return

        if not level_1_id in self.tree_data[level_0_id]["children"]:
            return

        self.tree_data[level_0_id]["children"][level_1_id]["children"] = odict()
        for entry in data:
            self.tree_data[level_0_id]["children"][level_1_id]["children"][entry['id']] = entry

    def remove_level_2(self, level_1_id, level_0_id):
        del self.tree_data[level_0_id]["children"][level_1_id]["children"]


    def init_transaction(self):
        self.add_level_0(self.load_level_0())

    def load_level_0(self, search_string=None, filter_key=None):
        return []

    def load_level_1(self, upper_leaf_id, search_string=None, filter_key=None):
        return []

    def load_level_2(self, upper_leaf_id, search_string=None, filter_key=None):
        return []

    def rebuild_tree_structure(self):
        search_string = self.search_string
        filter_key = self.filter_key
        self.reset_tree_data()

        self.add_level_0(self.load_level_0(search_string, filter_key))

        for leafid in self.open_leaf_0_ids:
            self.add_level_1(self.load_level_1(leafid, search_string, filter_key), leafid)

        for leaf_obj in self.open_leaf_1_ids.iteritems():
            self.add_level_2(self.load_level_2(leaf_obj[1]["leafid"], search_string, filter_key),
                             leaf_obj[1]["leafid"], leaf_obj[1]["parent_id"])

        self.redraw()


    def leaf_0_clicked(self, leafid):
        pass

    def handle_leaf_0_open(self, leafid, scroll_top):
        self.scroll_top = scroll_top
        leafid = int(leafid)

        self.add_level_1(self.load_level_1(leafid), leafid)
        self.open_leaf_0_ids.append(leafid)

        self.leaf_0_clicked(leafid)

        self.redraw()


    def handle_leaf_0_close(self, leafid, scroll_top):
        self.scroll_top = scroll_top
        leafid = int(leafid)

        self.open_leaf_0_ids.remove(leafid)
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

        del self.open_leaf_1_ids[leafid]
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

    def handle_drop(self, drag_leafid, drag_parent_leafid, drag_tree_cid, drop_leafid, drop_parent_leafid,
                    drop_tree_cid):
        pass




