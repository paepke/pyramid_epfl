# * encoding: utf-8

from solute.epfl.components.form.form import FormInputBase


class DatetimeInput(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:datetime_input/static", "datetime_input.js"),
                                       ("solute.epfl.components:datetime_input/static", "moment-with-locales.min.js"),
                                       ("solute.epfl.components:datetime_input/static",
                                        "bootstrap-datetimepicker.min.js")]

    css_name = FormInputBase.css_name + [("solute.epfl.components:datetime_input/static",
                                          "bootstrap-datetimepicker.min.css")]
    template_name = "datetime_input/datetime_input.html"
    compo_state = FormInputBase.compo_state + ["date_format"]
    js_parts = []

    date_format = "LLL"  #: This is the date format from moment.js http://momentjs.com/

    new_style_compo = True
    compo_js_params = ['fire_change_immediately', 'date_format']
    compo_js_name = 'DatetimeInput'

    def __init__(self, page, cid,
                 date_format=None,
                 label=None,
                 name=None,
                 value=None,
                 placeholder=None,
                 readonly=None,
                 validation_error=None,
                 validation_type=None,
                 validation_helper=None,
                 mandetory=None,
                 input_focus=None,
                 fire_change_immediately=None,
                 compo_col=None,
                 label_col=None,
                 layout_vertical=None,
                 label_style=None,
                 input_style=None,
                 **extra_params):
        """Datetime Input using bootstrap datime picker and moment js

        :param date_format: #: This is the date format from moment.js http://momentjs.com/
        :param label: Optional label describing the input field
        :param name: An element without a name cannot have a value
        :param value: The actual value of the input element that is posted upon form submission
        :param placeholder: Placeholder text that can be displayed if supported by the input
        :param readonly: Set to true if input cannot be changed and is displayed in readonly mode
        :param validation_error: Set during call of :func:`validate` with an error message if validation fails
        :param validation_type: Form validation selector.
        :param validation_helper: Subclasses can add their own validation helper lamdbas in order to extend validation logic.
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form
        :param input_focus: Set focus on this input when component is displayed
        :param fire_change_immediately: Set to true if input change events should be fired immediately to the server. Otherwise, change events are fired upon the next immediate epfl event
        :param compo_col: Set the width of the complete input component (default: max: 12)
        :param label_col: Set the width of the complete input component (default: 2)
        :param layout_vertical: Set to true if label should be displayed on top of the input and not on the left before it
        :param label_style: Can be used to add additional css styles for the label
        :param input_style: Can be used to add additional css styles for the input
        """
        super(DatetimeInput, self).__init__(page=page, cid=cid,
                                            date_format=date_format,
                                            label=label,
                                            name=name,
                                            value=value,
                                            placeholder=placeholder,
                                            readonly=readonly,
                                            validation_error=validation_error,
                                            validation_type=validation_type,
                                            validation_helper=validation_helper,
                                            mandetory=mandetory,
                                            input_focus=input_focus,
                                            fire_change_immediately=fire_change_immediately,
                                            compo_col=compo_col,
                                            label_col=label_col,
                                            layout_vertical=layout_vertical,
                                            label_style=label_style,
                                            input_style=input_style,
                                            **extra_params)

