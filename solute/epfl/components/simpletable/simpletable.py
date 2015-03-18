# coding: utf-8
from solute.epfl.core import epflcomponentbase,epflutil

class SimpleTable(epflcomponentbase.ComponentBase):

    template_name = "simpletable/simpletable.html"
    
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["simpletable/simpletable.js"]

    asset_spec = "solute.epfl.components:simpletable/static"

    js_name = []
    css_name = ["bootstrap.min.css"]

    compo_state = ["table_data","table_head","title"]

    compo_config = []

    table_data = None
    table_head = None
    title = None

