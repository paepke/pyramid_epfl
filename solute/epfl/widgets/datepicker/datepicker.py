# -*- coding: utf-8 -*-

from solute.epfl.core import epflwidgetbase


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

    def update_data_source(self, data_source):
        widget_name = data_source.name

        field_value = data_source.form.raw_data.get(widget_name, None)

        if not field_value:
            try:
                field_value = data_source.field.data.strftime(DATE_FORMAT)
            except:
                field_value = ''

        data_source.field_value = field_value
        data_source.style = data_source.kwargs.get('style', '')
        data_source.class_ = data_source.kwargs.get('class_', '')
