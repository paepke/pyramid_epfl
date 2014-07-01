# -*- coding: utf-8 -*-

import datetime
from solute.epfl.core import epflwidgetbase, epflfieldbase


DATE_FORMAT = "%d.%m.%Y"


class DatepickerWidget(epflwidgetbase.WidgetBase):

    """ Displays an uneditable input field with an outpopping datepicker.
    """

    name = "datepicker"
    template_name = "datepicker/datepicker.html"
    asset_spec = "solute.epfl.widgets:datepicker/static"

    js_name = ["datepicker.js"]
    css_name = ["datepicker.css"]

    param_def = {"default_date": epflwidgetbase.OptionalDateType,
                 "min_date": epflwidgetbase.OptionalDateType,
                 "max_date": epflwidgetbase.OptionalDateType}

    input_type = "Text"

    def handle_ValueChange(self, value):
        self.field.process_formdata([value])

    def update_data_source(self, data_source):
        for key in self.param_def:
            param = data_source.params.get(key, None)
            if param and type(param) is datetime.date:
                try:
                    data_source.params[key] = param.strftime(DATE_FORMAT)
                except:
                    data_source.params[key] = None

        field_value = data_source.value
        if not field_value:
            try:
                field_value = data_source.field.data.strftime(DATE_FORMAT)
            except:
                field_value = ''

        data_source.value = field_value


class Datepicker(epflfieldbase.FieldBase):
    widget_class = DatepickerWidget
