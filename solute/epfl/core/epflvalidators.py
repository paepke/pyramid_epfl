from abc import abstractmethod


class ValidatorBase(dict):
    """Utility class providing error handling, parameter lookup and validation hooks.
    """

    errors = None

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Overwrite this method to provide the interface for a custom validator.
        """
        super(ValidatorBase, self).__init__(*args, **kwargs)

    def __call__(self, caller, *args, **kwargs):
        """Lookup parameters, run validation, return result.
        """
        self.caller = caller
        self.errors = []
        for key, value in self.iteritems():
            if type(value) is not str:
                kwargs[key] = value
                continue
            kwargs[key] = self.get_param(value)

        return self.validate(**kwargs)

    @abstractmethod
    def validate(self, **kwargs):
        """Abstract validate method to be called by __call__. Has to be overwritten with custom validation logic.
        """
        raise Exception("No validation implemented.")

    @property
    def error_message(self):
        """Error message handling allowing for multiple messages to be present to describe the current error state.
        """
        return '\n'.join(self.errors)

    @error_message.setter
    def error_message(self, value):
        """Appends value to the list of errors.
        """
        self.errors.append(value)

    @error_message.deleter
    def error_message(self):
        """Resets the list of errors.
        """
        self.errors = []

    def get_param(self, param_name):
        """Get a specific param as determined by its name from either the calling component or the appropriate target.
        Returns in this order: attribute param_name of target component, item param_name of target component, param_name
        on miss. Target component is the calling component if param_name is not dotted. Else the target component is
        looked up in the parent form by the name defined by the string preceding the dot.

        password.value: Lookup the field with the name password and return its attribute or item value.
        password.: Return the field with the name password.
        value: Return the attribute or item value of the calling component.

        :param param_name: The (dotted) name to lookup.
        """
        # Split param_name and lookup actual target if required.
        target, original_name = None, param_name
        if '.' in param_name:
            target, param_name = self.get_dotted(param_name)

        if param_name == '':
            return target

        if target is None:
            target = self.caller
        if hasattr(target, param_name):
            return getattr(target, param_name)

        return original_name

    def get_dotted(self, param_name):
        field_name, param_name = param_name.split('.')
        form = self.caller.get_parent_form()
        if form is None:
            raise Exception('No parent form found. Did you try using a dotted name on a Validator with no Form?')
        for sibling in form.registered_fields:
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
    def __init__(self, value='value', error_message='Value is required!', *args, **kwargs):
        """Validate a related Input field as a text.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        """
        super(TextValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, error_message=None, **kwargs):
        # Check if mandatory and present.
        if self.caller.mandatory and (value is None or value in ["", u'']):
            self.error_message = error_message
            return False

        return True


class EmailValidator(TextValidator):
    def __init__(self, value='value', error_message='E-Mail is required!', domain=None,
                 error_message_domain='Invalid domain!', *args, **kwargs):
        """Validate a related Input field as a text.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        :param domain: List of domains accepted by this validator instance.
        :param error_message_domain: Error message to be displayed upon encountering a wrong domain.
        """
        super(EmailValidator, self).__init__(value=value, error_message=error_message, domain=domain,
                                             error_message_domain=error_message_domain, *args, **kwargs)

    def validate(self, value=None, error_message=None, domain=None, error_message_domain=None, **kwargs):
        result = super(EmailValidator, self).validate(value=value, error_message=error_message,
                                                      error_message_domain=error_message_domain, **kwargs)
        if result is False:
            return False

        if value is not None and value not in ["", u'']:
            if '@' not in value:
                self.error_message = error_message
                return False
            split_value = value.split('@')
            if len(split_value) != 2:
                self.error_message = error_message
                return False

            if domain is not None and split_value[1] not in domain:
                self.error_message = error_message_domain
                return False

        return True


class NumberValidator(ValidatorBase):
    float = False  #: Treat value as a float.

    def __init__(self, value='value', min_value=None, max_value=None, error_message='Value is required!', *args,
                 **kwargs):
        """Validate a related Input field as a number.

        :param value: Where to get the value to be evaluated.
        :param min_value: Lower boundary for value.
        :param max_value: Upper boundary for value.
        :param error_message: Error message to be displayed upon failed validation. If left to default with either
                              min_value or max_value present this will default to 'Value is outside of limit' instead.
        """
        if (min_value or max_value) and error_message == 'Value is required!':
            error_message = 'Value is outside of limit!'
        super(NumberValidator, self).__init__(value=value, error_message=error_message, *args, **kwargs)

    def validate(self, value=None, min_value=None, max_value=None, error_message=None, **kwargs):
        # Check if mandatory and present.
        if self.caller.mandatory and (value is None or value == ""):
            self.error_message = error_message
            return False

        # Not mandatory and not set passes muster.
        if value is None or value == "":
            return True

        # Can value be cast to float or int respectively.
        try:
            if self.float:
                float(value)
            else:
                int(value)
        except ValueError:
            self.error_message = error_message
            return False

        # Ensure value is within boundaries of min_value and max_value respectively.
        if min_value is not None and int(value) < min_value:
            self.error_message = error_message
            return False
        elif max_value is not None and int(value) > max_value:
            self.error_message = error_message
            return False

        return True


class FloatValidator(NumberValidator):
    float = True  #: Just set this to True and NumberValidator will do the rest.


VALIDATOR_MAP = {
    'email': EmailValidator,
    'text': TextValidator,
    'number': NumberValidator,
    'float': FloatValidator,
}
