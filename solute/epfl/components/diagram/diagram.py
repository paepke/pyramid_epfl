# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
import json

class Diagram(epflcomponentbase.ComponentBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "diagram/diagram.html"
    asset_spec = "solute.epfl.components:diagram/static"

    js_name = ["highcharts.js", "exporting.js", "export-csv-1.2.1.js"]

    
    compo_config = []
    compo_state = []
    
    diagram_params = {}
    
    def get_params(self):
        return self.diagram_params
    def set_params(self, params):
        self.diagram_params = params

    def __init__(self, label=None, value=None, callback=None, **extra_params):
        super(Diagram, self).__init__()
        self.diagram_params = {}
