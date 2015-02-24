from solute.epfl.core import epflcomponentbase

class Selectize(epflcomponentbase.ComponentBase):
    """
    Dropdown with optgroups and search function with highlighting

    The entries are set in this format

    .. code:: python

        entries = [{"name": "Group4", "entries": [{"id" : "entry1_id", "value": "entry1" }, {"id" : "entry2_id", "value": "entry2" }, ...]},
               {"name": "Group5", "entries": [{"id" : "entry3_id", "value": "entry3" }, ...]},
               {"name": "Group6", "entries": [{"id" : "entry4_id", "value": "entry4" }, ...]}]

    """

    template_name = "selectize/selectize.html"

    js_parts = epflcomponentbase.ComponentBase.js_parts + ["selectize/selectize.js"]
    asset_spec = "solute.epfl.components:selectize/static"

    css_name = ["selectize.css"]
    js_name = ["selectize.js"]

    compo_config = []
    compo_state = ["entries", "selection_id", "label"]

    entries = []
    selection_id = ""  #:the current selection, this is the last value which was selected with enter or mouseclick
    label = None
    layout_vertical = False

    def handle_set_selection(self, selection_id, selection_text):
        self.selection_id = selection_id
