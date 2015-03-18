from solute.epfl.core import epflcomponentbase
from solute.epfl.components.form.form import FormInputBase


class Selectize(FormInputBase):
    """
    Dropdown with optgroups and search function with highlighting

    The entries are set in this format

    .. code:: python

        entries = [{"name": "Group4", "entries": [{"id" : "entry1_id", "value": "entry1" }, {"id" : "entry2_id", "value": "entry2" }, ...]},
               {"name": "Group5", "entries": [{"id" : "entry3_id", "value": "entry3" }, ...]},
               {"name": "Group6", "entries": [{"id" : "entry4_id", "value": "entry4" }, ...]}]

    """

    template_name = "selectize/selectize.html"

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['selectize/selectize.js'])
    js_name = FormInputBase.js_name + [("solute.epfl.components:selectize/static", "selectize.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:selectize/static", "selectize.css")]


    compo_config = []
    compo_state = FormInputBase.compo_state + ["entries","drop_down_height","selected_text"]

    entries = None
    layout_vertical = False
    drop_down_height = None
    selected_text = None

    def handle_set_selection(self, selection_id, selection_text):
        self.value = selection_id
        self.selected_text = selection_text

    def validate(self):
        if self.mandatory and ((self.value is None) or (self.value == "")):
            self.validation_error = 'Value is required'
            self.redraw()
            return False

        self.validation_error = ''
        return True