# * encoding: utf-8

from solute.epfl.components.text_input.text_input import TextInput


class DatetimeInput(TextInput):
    #: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)
    date = True

    def __init__(self, page, cid, date=True, **extra_params):
        """ Datetime input this is a convenience component for textinput which overrides the date flag to true,

        :param date: Set to true if input field should be a datetime picker (using jquery-datetimepicker plugin)
        """
        super(DatetimeInput, self).__init__(page, cid, date=date, **extra_params)
