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

    js_name = FormInputBase.js_name + [("solute.epfl.components:selectize/static", "selectize.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:selectize/static", "selectize.css")]

    compo_config = []
    compo_state = FormInputBase.compo_state + ["entries", "drop_down_height", "selected_text", "search_server_side",
                                               "search_text","cursor_position"]

    entries = None
    layout_vertical = False
    drop_down_height = None
    selected_text = None

    search_server_side = False
    search_text = ""

    cursor_position = 0

    new_style_compo = True
    compo_js_name = 'Selectize'
    compo_js_params = ['fire_change_immediately', "search_server_side", "search_text", "input_focus",
                       "cursor_position", "selected_text"]
    #compo_js_extras = ['handle_click']


    def handle_update_search(self, search_text,cursor_position):
        self.search_text = search_text
        self.cursor_position = cursor_position
        self.entries = self.reload_entries(search_text)
        self.selected_text = None
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

    def load_data_async(self):
        #; overwrite me
        return []

