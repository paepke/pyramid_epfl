from solute.epfl.core import epflcomponentbase

class Selectize(epflcomponentbase.ComponentBase):
    """
    Dropdown with optgroups and search function with highlighting

    The entries are set in this format

    .. code:: python

        entries = [{"name": "Group4", "entries": ["entry1", "entry2", "entry3", "entry4", "entry5", "entry6"]},
               {"name": "Group5", "entries": ["entry1", "entry2", "entry3", "entry4", "entry5", "entry6"]},
               {"name": "Group6", "entries": ["entry1", "entry2", "entry3", "entry4", "entry5", "entry6"]}]

    """

    template_name = "selectize/selectize.html"

    js_parts = epflcomponentbase.ComponentBase.js_parts + ["selectize/selectize.js"]
    asset_spec = "solute.epfl.components:selectize/static"

    css_name = ["selectize.css"]
    js_name = ["selectize.js"]

    compo_config = []
    compo_state = ["entries", "selection"]

    entries = []
    selection = ""  #:the current selection, this is the last value which was selected with enter or mouseclick

    def handle_set_selection(self, selection):
        self.selection = selection
