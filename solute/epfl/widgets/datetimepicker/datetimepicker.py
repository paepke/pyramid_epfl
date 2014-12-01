# -*- coding: utf-8 -*-

import datetime
from solute.epfl.core import epflwidgetbase, epflfieldbase, epfli18n


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


    def setup_type(self):
        """ handles the different data-types for this field.
        It manages the coerceion-function. """

        if self.field_type == "char":
            super(Datetimepicker, self).setup_type()
        elif self.field_type.startswith("char("):
            super(Datetimepicker, self).setup_type()
        elif self.field_type == "int":
            super(Datetimepicker, self).setup_type()
        elif self.field_type == "float":
            super(Datetimepicker, self).setup_type()
        elif self.field_type in ["isodatetime", "isodate", "isotime"]:
            self.coerce_func = coerce_func_isodate
            self.visualize_func = visualize_func_isodate
            self.coerce_error_msg = "txt_incorrect_isodate"
        else:
            raise TypeError, "Field-Type " + repr(self.__class__.__name__) + " does not support type: " + repr(self.field_type)


def coerce_func_isodate(request, data):


    if data is None:
        return None
    elif not unicode(data).strip():
        return None
    else:

        # first, check if it's already ISO-format!
        iso_format = True
        try:
            iso_time = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            try:
                iso_time = datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                iso_format = False

        if iso_format:
            return data
        else:
            iso_time = epfli18n.convert_to_isodate(request, data, format = "%d.%m.%Y %H:%M")
            return iso_time

def visualize_func_isodate(field):
    time = field.data

    if time:
        time_str = epfli18n.format_isodate(field.form.request, field.data, format = "%d.%m.%Y %H:%M")
        return unicode(time_str)
    else:
        return u""
