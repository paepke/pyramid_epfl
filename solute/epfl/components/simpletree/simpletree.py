# coding: utf-8

from solute.epfl.core import epflcomponentbase


class Simpletree(epflcomponentbase.ComponentBase):
    template_name = "simpletree/simpletree.html"
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletree/simpletree.js"]

    asset_spec = "solute.epfl.components:simpletree/static"

    js_name = ["simpletree.js"]

    css_name = ["simpletree.css"]

    compo_config = []
    compo_state = ["tree_data", "search_string", "open_leaf_0_ids", "open_leaf_1_ids", "all_filter", "filter_key","scroll_top"]

    tree_data = {}

    open_leaf_0_ids = []
    open_leaf_1_ids = {}
    all_filter = []

    height = 400

    search_string = None
    filter_key = None

    scroll_top = 0

    # TREE DATA
    def reset_tree_data(self):
        self.tree_data = {}

    def add_level_0(self, data):
        for entry in data:
            self.tree_data[entry['id']] = entry


    def add_level_1(self, data, parent_id):
        self.tree_data[parent_id]["children"] = {}
        for entry in data:
            self.tree_data[parent_id]["children"][entry['id']] = entry

    def remove_level_1(self, parent_id):
        del self.tree_data[parent_id]["children"]


    def add_level_2(self, data, level_1_id, level_0_id):
        if (not self.tree_data[level_0_id].has_key("children")):
            return

        if(not self.tree_data[level_0_id]["children"].has_key(level_1_id)):
            return

        self.tree_data[level_0_id]["children"][level_1_id]["children"] = {}
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


    def handle_leaf_0_clicked(self, leafid,scroll_top):
        self.scroll_top = scroll_top
        leafid = int(leafid)

        if leafid in self.open_leaf_0_ids:
            # close
            self.open_leaf_0_ids.remove(leafid)
            self.remove_level_1(leafid)
        else:
            # open
            self.add_level_1(self.load_level_1(leafid), leafid)
            self.open_leaf_0_ids.append(leafid)

        self.redraw()


    def handle_leaf_1_clicked(self, leafid, parent_id,scroll_top):
        self.scroll_top = scroll_top
        if leafid in self.open_leaf_1_ids:
            # close
            del self.open_leaf_1_ids[leafid]
            self.remove_level_2(leafid, parent_id)

        else:
            # open
            self.add_level_2(self.load_level_2(leafid), leafid, parent_id)
            self.open_leaf_1_ids[leafid] = {"leafid": leafid, "parent_id": parent_id}

        self.redraw()

    def handle_leaf_2_clicked(self, leafid,scroll_top):
        self.scroll_top = scroll_top
        # Overwrite for click handling
        pass


    def handle_search(self, search_string, filter_key):
        self.search_string = search_string
        self.filter_key = filter_key
        self.rebuild_tree_structure()

    def rebuild_tree_structure(self):
        search_string = self.search_string
        filter_key = self.filter_key
        self.reset_tree_data()

        self.add_level_0(self.load_level_0(search_string, filter_key))

        print "self.open_leaf_0_ids",self.open_leaf_0_ids
        print "self.open_leaf_1_ids",self.open_leaf_1_ids

        for leafid in self.open_leaf_0_ids:
            self.add_level_1(self.load_level_1(leafid, search_string, filter_key), leafid)

        for leaf_obj in self.open_leaf_1_ids.iteritems():
            self.add_level_2(self.load_level_2(leaf_obj[1]["leafid"], search_string, filter_key),
                             leaf_obj[1]["leafid"],leaf_obj[1]["parent_id"])

        self.redraw()

    def handle_drop(self, drag_leafid, drag_parent_leafid, drag_tree_cid, drop_leafid, drop_parent_leafid,
                    drop_tree_cid):
        pass




