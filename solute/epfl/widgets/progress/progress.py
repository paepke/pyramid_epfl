#-*- coding: utf-8 -*-

from solute.epfl.core import epflfieldbase
from solute.epfl.core import epflwidgetbase

class ProgressWidget(epflwidgetbase.WidgetBase):
    """ Displays an accordion which allows
    """

    name = "progress"
    template_name = "progress/progress.html"
    asset_spec = "solute.epfl.widgets:progress/static"

    js_name = ["progress.js"]
    css_name = ["progress.css"]


    param_def = { "max": epflwidgetbase.NumberType }

    def handle_ValueChange(self, value):
        self.field.process_formdata([value])

class Progress(epflfieldbase.FieldBase):
    widget_class = ProgressWidget
