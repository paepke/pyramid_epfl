# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
import json


class Diagram(epflcomponentbase.ComponentBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "diagram/diagram.html"
    js_parts = "diagram/diagram.js"
    asset_spec = "solute.epfl.components:diagram/static"

    js_name = ["highcharts.js", "exporting.js",
               "export-csv-1.2.1.js", "diagram.js"]

    compo_config = []
    compo_state = ["diagram_params"]

    diagram_params = {}

    def get_params(self):
        return self.diagram_params

    def set_params(self, params):
        self.diagram_params = params

    def handle_visibilityChange(self, series_visibility):
        if not "series" in self.diagram_params:
            return
        for series_visibility_entry in series_visibility:
            if "name" in series_visibility_entry:
                for backed_series_entry in self.diagram_params["series"]:
                    if backed_series_entry["name"] == series_visibility_entry["name"]:
                        if ("visible" in series_visibility_entry) and (series_visibility_entry["visible"] == False):
                            backed_series_entry["visible"] = False
                        elif "visible" in backed_series_entry:
                            backed_series_entry.pop("visible")

    
