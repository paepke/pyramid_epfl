from solute.epfl.core import epflcomponentbase
from solute.epfl.components import Droppable, Dragable
from odict import odict


class FormBaseComponent(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:form/static"

    compo_state = ['name', 'value', 'validation_error']

    # An element without a name cannot have a value.
    name = None
    value = None
    validation_error = ''
    validation_type = None
    validation_helper = []
    mandatory = False

    def is_numeric(self):
        return type(self.value) in [int, float]

    def init_transaction(self):
        super(FormBaseComponent, self).init_transaction()

        def get_parent_form(compo):
            if isinstance(compo, Form):
                return compo
            if not hasattr(compo, 'container_compo'):
                return None
            return compo.container_compo

        # try to find a parent form and register this component, but fail silently,
        # since components do not need to be nested inside a form
        try:
            get_parent_form(self.container_compo).register_field(self)
        except AttributeError:
            pass

    def get_value(self):
        """
        Return the field value without conversions.
        """
        return self.value

    def validate(self):
        """
        Validate the value and return True if it is correct or False if not. Set error messages to self.validation_error
        """
        result, text = True, ''
        if self.validation_type == 'text':
            if self.mandatory and ((self.value is None) or (self.value == "")):
                result, text = False, 'Value is required'
        elif self.validation_type == 'number':
            if self.mandatory and ((self.value is None) or (self.value == "")):
                result, text = False, 'Value is required'
            elif ((not self.value is None) and (self.value != "")):
                try:
                    int(self.value)
                except ValueError:
                    result, text = False, 'Value did not validate as number.'
        # validation_type bool is always valid

        for helper in self.validation_helper:
            if not result:
                break
            result, text = helper[0](self), helper[1]

        if not result:
            self.redraw()
            self.validation_error = text
            return False

        if self.validation_error:
            self.redraw()
        self.validation_error = ''

        return True

    @property
    def converted_value(self):
        if self.validation_type == 'text':
            return str(self.value)
        if self.validation_type == 'number':
            return int(self.value)
        if self.validation_type == 'bool':
            return bool(self.value)
        return self.value

    def handle_change(self, value):
        self.value = value



class Form(epflcomponentbase.ComponentContainerBase):
    template_name = "form/form.html"
    js_parts = "form/form.js"

    asset_spec = "solute.epfl.components:form/static"

    compo_state = ["_registered_fields"]

    fields = []
    _registered_fields = []
    validation_errors = []

    validate_hidden_fields = False

    def __init__(self, node_list=None, validate_hidden_fields=False, **extra_params):
        super(Form, self).__init__()

    def handle_submit(self):
        pass

    def register_field(self, field):
        self._registered_fields.append(field.cid)

    @property
    def registered_fields(self):
        return [self.page.components[cid] for cid in self._registered_fields]

    def get_values(self):
        values = odict()
        for field in self.registered_fields:
            if field.name is None:
                continue
            values[field.name] = field.converted_value
        return values

    def set_value(self, key, value):
        for field in self.registered_fields:
            if field.name == key:
                field.value = value
                return

    def validate(self):
        result = []
        for field in self.registered_fields[:]:
            # Do not validate fields without a name, cause they can not contain
            # a value.
            if field.name is None:
                continue
            if not self.validate_hidden_fields and not field.is_visible():
                continue
            validation_result = field.validate()
            result.append(validation_result)

        if False in result:
            self.validation_errors = result
        return not False in result

    def get_errors(self):
        return self.validation_errors
