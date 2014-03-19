# -*- coding: utf-8 -*-

from solute.epfl.core import epflwidgetbase

class SliderWidget(epflwidgetbase.WidgetBase):


    """ Displays a horizontal slider element.
    min_value and max_value can be integer or float
    on_change can be a event-handler-name or "submit" which then submittes the complete form

    Additional jinja-attributes:

    {{ field.value_box }}: If used in template it shows the current value of the slider

    """


    name = "slider"
    template_name = "slider/slider.html"
    asset_spec = "solute.epfl.widgets:slider/static"

    js_name = ["slider.js"]
    css_name = []

    param_def = {"min_value": epflwidgetbase.NumberType,
                 "max_value": epflwidgetbase.NumberType,
                 "on_change": epflwidgetbase.EventType}


    def update_data_source(self, data_source):

        if type(data_source.params["min_value"]) is float:
            data_source.value_divisor = 10000
            data_source.params["min_value"] *= data_source.value_divisor
            data_source.params["max_value"] *= data_source.value_divisor
        else:
            data_source.value_divisor = 1

    def pre_render(self):
        super(SliderWidget, self).pre_render()

        self.field.value_box = "<div id='" + self.field.name + "_value_box'></div>"
