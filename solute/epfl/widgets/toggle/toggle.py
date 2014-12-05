# -*- coding: utf-8 -*-

from solute.epfl.core import epflfieldbase
from solute.epfl.core import epflwidgetbase

class ToggleWidget(epflwidgetbase.WidgetBase):
    """ Displays an accordion which allows
    """

    name = "toggle"
    template_name = "toggle/toggle.html"
    asset_spec = "solute.epfl.widgets:toggle/static"

    js_name = ["toggle.js","bootstrap-switch.min.js"]
    css_name = ["toggle.css","bootstrap.min.css", "bootstrap-switch.min.css"]


    param_def = {"on": epflwidgetbase.StringType,
                 "off": epflwidgetbase.StringType,
                 }

    def handle_ValueChange(self, value):
        self.field.process_formdata([value])

class Toggle(epflfieldbase.FieldBase):
    widget_class = ToggleWidget
