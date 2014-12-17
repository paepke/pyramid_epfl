from solute.epfl.core import epflcomponentbase


class FormBaseComponent(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:form_components/static"

    # An element without a name can not have a value.
    name = None
    value = None
    validation_error = ''
    validation_type = None

    def init_transaction(self):
        super(FormBaseComponent, self).init_transaction()

        def get_parent_form(compo):
            if isinstance(compo, Form):
                return compo
            if not hasattr(compo, 'container_compo'):
                return None
            return compo.container_compo

        get_parent_form(self.container_compo).register_field(self)

    def get_value(self):
        """
        Return the field value without conversions.
        """
        return self.value

    def validate(self):
        """
        Validate the value and return True if it is correct or False if not. Set error messages to self.validation_error
        """
        if self.validation_type == 'text':
            return type(self.converted_value) is str
        if self.validation_type == 'number':
            return type(self.converted_value) is int
        return False

    @property
    def converted_value(self):
        if self.validation_type == 'text':
            return str(self.value)
        if self.validation_type == 'number':
            return int(self.value)
        return self.value

class Input(FormBaseComponent):
    template_name = "form_components/form.input.html"

    label = None
    name = None
    value = None
    link = None
    input_type = None

    def __init__(self, input_type=None, label=None, name=None, link=None, value="", validation_type="", **extra_params):
        super(Input, self).__init__()


class Button(FormBaseComponent):
    template_name = "form_components/form.button.html"

    label = None
    value = None
    callback = None

    def __init__(self, label=None, value=None, callback=None, **extra_params):
        super(Button, self).__init__()


class Form(epflcomponentbase.ComponentTreeBase):
    template_name = "form_components/form.html"
    asset_spec = "solute.epfl.components:form_components/static"

    css_name = ["bootstrap.min.css"]
    compo_state = ["_registered_fields"]

    fields = []
    _registered_fields = []

    validate_hidden_fields = False

    def __init__(self, fields=None, validate_hidden_fields=False, **extra_params):
        super(Form, self).__init__()

    def init_tree_struct(self):
        return self.fields

    def register_field(self, field):
        self._registered_fields.append(field.cid)

    @property
    def registered_fields(self):
        return [getattr(self.page, cid) for cid in self._registered_fields]

    def get_values(self):
        values = []
        for field in self.registered_fields:
            if field.name is None:
                continue
            values.append((field.name, field.converted_value))
        return values

    def validate(self):
        result = []
        for field in self.registered_fields:
            # Do not validate fields without a name, cause they can not contain a value.
            if field.name is None:
                continue
            if not self.validate_hidden_fields and not field.is_visible():
                continue
            result.append(field.validate())
        return not False in result, result