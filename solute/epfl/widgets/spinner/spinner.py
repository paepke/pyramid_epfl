# -*- coding: utf-8 -*-

from solute.epfl.core import epflfieldbase
from solute.epfl.core import epflwidgetbase

class SpinnerWidget(epflwidgetbase.WidgetBase):
    """ Displays an accordion which allows
    """

    name = "spinner"
    template_name = "spinner/spinner.html"
    asset_spec = "solute.epfl.widgets:spinner/static"

    js_name = ["spinner.js"]
    css_name = ["spinner.css"]


    param_def = {"step": epflwidgetbase.NumberType,
                 "min": epflwidgetbase.NumberType,
                 "max": epflwidgetbase.NumberType,
                 }

    def handle_ValueChange(self, value):
        self.field.process_formdata([value])

class Spinner(epflfieldbase.FieldBase):
    widget_class = SpinnerWidget
