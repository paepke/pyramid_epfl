from solute.epfl.core import epflcomponentbase
from solute.epfl.components.form.form import FormInputBase


class Selectize(FormInputBase):
    """
    Dropdown with optgroups and search function with highlighting

    The entries are set in this format

    .. code:: python

        entries = [{"value": "Group4",id:0 "entries": [{"id" : "entry1_id", "value": "entry1" }, {"id" : "entry2_id", "value": "entry2" }, ...]},
               {"value": "Group5",id:1 , "entries": [{"id" : "entry3_id", "value": "entry3" }, ...]},
               {"value": "Group6",id:2 , "entries": [{"id" : "entry4_id", "value": "entry4" }, ...]}]

    """

    template_name = "selectize/selectize.html"

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['selectize/selectize.js'])
    js_name = FormInputBase.js_name + [("solute.epfl.components:selectize/static", "selectize.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:selectize/static", "selectize.css")]

    compo_config = []
    compo_state = FormInputBase.compo_state + ["entries", "drop_down_height", "selected_text", "search_server_side",
                                               "search_text","load_asnyc","is_loading","cursor_position"]

    entries = None
    layout_vertical = False
    drop_down_height = None
    selected_text = None

    search_server_side = False
    search_text = ""

    load_async = False
    is_loading = False

    cursor_position = 0

    def handle_update_search(self, search_text,cursor_position):
        self.search_text = search_text
        self.cursor_position = cursor_position
        self.entries = self.reload_entries(search_text)
        self.redraw()

    def reload_entries(self, search):
        """
        Overwrite me if you use serach_server_side true
        Return values in the entries format
        """
        return []

    def handle_set_selection(self, selection_id, selection_value, selection_group_id, selection_group_value):
        self.value = selection_id
        self.selected_text = selection_value

    def validate(self):
        if self.mandatory and ((self.value is None) or (self.value == "")):
            self.validation_error = 'Value is required'
            self.redraw()
            return False

        self.validation_error = ''
        return True

    def init_transaction(self):
        if self.load_async:
            self.is_loading = True
            self.add_js_response("epfl.Selectize.LoadData('%s')" % self.cid);
            self.load_async = False

    def handle_load_data(self):
        self.entries = self.load_data_async()
        self.is_loading = False
        self.redraw()

    def load_data_async(self):
        #; overwrite me
        return []

