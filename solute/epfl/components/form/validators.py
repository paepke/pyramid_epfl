#* coding: utf-8

from wtforms.validators import ValidationError
from datetime import datetime


class Date():
    def __init__(self, format='%d.%m.%Y', message=None):
        self.format = format

        if not message:
            message = u'Field must be a date in the form %s' % self.format

        self.message = message

    def __call__(self, form, field):
        user_input = field.data

        try:
            datetime.strptime(user_input, self.format)
        except:
            raise ValidationError(self.message)


class DateBetween():
    def __init__(self, format='%d.%m.%Y', start_date=None, end_date=None, not_between_message=None):

        if not start_date and not end_date:
            raise Exception('DateBetween validator: at least one date parameter has to be provided')

        if start_date and type(start_date) is not datetime:
            raise Exception('DateBetween validator: start_date has be of type datetime.datetime')

        if end_date and type(end_date) is not datetime:
            raise Exception('DateBetween validator: end_date has be of type datetime.datetime')

        if start_date and end_date and start_date > end_date:
            raise Exception('DateBetween validator: start_date after end_date is not allowed')

        self.start_date = start_date
        self.end_date = end_date
        self.format = format

        if not not_between_message:
            not_between_message = u'Field date is out of valid period'

        self.not_between_message = not_between_message

    def __call__(self, form, field):
        user_input = field.data
        input_date = None
        start_date = self.start_date
        end_date = self.end_date

        try:
            input_date = datetime.strptime(user_input, self.format)
        except:
            return

        if start_date and input_date < start_date:
            raise ValidationError(self.not_between_message)

        if end_date and input_date > end_date:
            raise ValidationError(self.not_between_message)


class DecimalCommaOrDot():
    def __init__(self, message=None):
        if not message:
            message = u'Field must be a numeric type with a comma or dot as decimal seperator'

        self.message = message

    def __call__(self, form, field):
        user_input = field.data

        if user_input and ',' not in user_input:
            try:
                field.data = float(user_input)
            except:
                raise ValidationError(self.message)
        elif user_input and ',' in user_input:
            try:
                user_input = user_input.replace(',', '.')
                field.data = float(user_input)
            except:
                raise ValidationError(self.message)
        else:
            raise ValidationError(self.message)


class AutocompleteRequired():
    def __init__(self, message=None):
        if not message:
            message = u'This field is required!'

        self.message = message

    def __call__(self, form, field):
        user_input = field.data

        if not user_input or user_input == 'None':
            raise ValidationError(self.message)
