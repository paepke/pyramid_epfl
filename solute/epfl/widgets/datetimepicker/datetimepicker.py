# -*- coding: utf-8 -*-

import datetime
from solute.epfl.core import epflwidgetbase, epflfieldbase


DATE_FORMAT = "%d.%m.%Y"
TIME_FORMAT = "%H:%M"
DATE_TIME_FORMAT = "%d.%m.%Y %H:%M"


class DatetimepickerWidget(epflwidgetbase.WidgetBase):

    """ Displays an uneditable input field with an outpopping datetimepicker.
    """

    name = "datetimepicker"
    template_name = "datetimepicker/datetimepicker.html"
    asset_spec = "solute.epfl.widgets:datetimepicker/static"

    js_name = ["jquery.datetimepicker.js",
               "datetimepicker.js"]

    css_name = ["jquery.datetimepicker.css"]

    param_def = {#Datepicker options
                 "datepicker": (epflwidgetbase.OptionalBooleanType, True),
                 "minDate": epflwidgetbase.OptionalDateType,
                 "maxDate": epflwidgetbase.OptionalDateType,
                 "startDate": epflwidgetbase.OptionalDateType,

                 #Timepicker options
                 "timepicker": (epflwidgetbase.OptionalBooleanType, True),
                 "minTime": epflwidgetbase.OptionalTimeType,
                 "maxTime": epflwidgetbase.OptionalTimeType,
                 "allowTimes": epflwidgetbase.OptionalDomainType,
                 "step": epflwidgetbase.NumberType
                 }


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
            if param and type(param) is datetime.time:
                try:
                    data_source.params[key] = param.strftime(TIME_FORMAT)
                except:
                    data_source.params[key] = None

        field_value = data_source.value

        if not field_value:
            try:
                field_value = data_source.field.data.strftime(DATE_FORMAT)
            except:
                try:
                    field_value = data_source.field.data.strftime(TIME_FORMAT)
                except:
                    try:
                        field_value = data_source.field.data.strftime(DATE_TIME_FORMAT)
                    except:
                        field_value = ''

        data_source.value = field_value

class Datetimepicker(epflfieldbase.FieldBase):
    widget_class = DatetimepickerWidget
