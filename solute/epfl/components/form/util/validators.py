from abc import abstractmethod


class ValidatorBase(dict):
    errors = None

    def __init__(self, *args, **kwargs):
        super(ValidatorBase, self).__init__(*args, **kwargs)

    def __call__(self, caller, *args, **kwargs):
        self.caller = caller
        self.errors = []
        for k, v in self.iteritems():
            if type(v) is not str:
                continue
            kwargs[k] = self.get_param(v)

        return self.validate(**kwargs)

    @abstractmethod
    def validate(self, **kwargs):
        raise Exception("No validation implemented.")

    @property
    def form(self):
        return self.caller.get_parent_form()

    @property
    def error_message(self):
        return '\n'.join(self.errors)

    @error_message.setter
    def error_message(self, value):
        self.errors.append(value)

    def get_param(self, param_name, target=None):
        original_name = param_name
        if '.' in param_name:
            target, param_name = self.get_dotted(param_name)

        if param_name == '':
            return target

        if target is None:
            target = self.caller
        if hasattr(target, param_name):
            return getattr(target, param_name)

        try:
            return target.get(param_name, original_name)
        except AttributeError:
            return original_name

    def get_dotted(self, param_name):
        field_name, param_name = param_name.split('.')

        for sibling in self.form.registered_fields:
            if sibling.name == field_name:
                return sibling, param_name

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, data):
        self.update(data)

    @classmethod
    def by_name(cls, name):
        return VALIDATOR_MAP.get(name, ValidatorBase)


class TextValidator(ValidatorBase):
    def __init__(self, value='value', error_message='Value is required', *args, **kwargs):
        super(TextValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, error_message=None, **kwargs):
        if self.caller.mandatory and (value is None or value == ""):
            self.error_message = error_message
            return False


class NumberValidator(ValidatorBase):
    float = False

    def __init__(self, value='value', min_value=None, max_value=None, error_message='Value is required', *args,
                 **kwargs):
        if (min_value or max_value) and error_message == 'Value is required':
            error_message = 'Value is outside of limit'
        super(NumberValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, min_value=None, max_value=None, error_message=None, **kwargs):
        if self.caller.mandatory and (value is None or value == ""):
            self.error_message = error_message
            return False
        if value is not None and value != "":
            try:
                if self.float:
                    float(value)
                else:
                    int(value)
            except ValueError:
                self.error_message = error_message
                return False
            if min_value is not None and int(value) < min_value:
                self.error_message = error_message
                return False
            elif max_value is not None and int(value) > max_value:
                self.error_message = error_message
                return False
        return True


class FloatValidator(NumberValidator):
    float = True


VALIDATOR_MAP = {
    'text': TextValidator,
    'number': NumberValidator,
    'float': FloatValidator,
}
