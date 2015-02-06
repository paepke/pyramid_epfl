from solute.epfl.core import epflcomponentbase
from solute.epfl.components import Droppable, Dragable
from collections2 import OrderedDict as odict


class FormInputBase(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:form/static"

    compo_state = ['label', 'name', 'value', 'validation_error']
    js_parts = ["form/input_base.js"]

    js_name = ["input_base.js", "bootstrap3-typeahead.min.js"]
    css_name = ["input_base.css"]

    label = None  #: Optional label describing the input field.
    name = None  #: An element without a name cannot have a value.
    value = None  #: The actual value of the input element that is posted upon form submission.
    default = None  #: Default value that may be pre-set or pre-selected
    placeholder = None  #: Placeholder text that can be displayed if supported by the input.
    #: Set during call of :func:`validate` with an error message if validation fails.
    validation_error = ''
    validation_type = None
    #: Subclasses can add their own validation helper lamdbas in order to extend validation logic.
    validation_helper = []
    #: Set to true if value has to be provided for this element in order to yield a valid form.
    mandatory = False
    typeahead = False  # : Set to true if typeahead should be provided by the input (if supported)
    #: If true, underlying form is submitted upon enter key in this input
    submit_form_on_enter = False
    input_focus = False  # : Set focus on this input when component is displayed
    #: Set to true if input change events should be fired immediately to the server.
    #: Otherwise, change events are fired upon the next immediate epfl event.
    fire_change_immediately = False

    def __init__(self, label=None, name=None, typeahead=False, default="", validation_type="",
                 **extra_params):
        super(FormInputBase, self).__init__()

    def is_numeric(self):
        return type(self.value) in [int, float]

    def init_transaction(self):
        super(FormInputBase, self).init_transaction()

        if self.value is None and self.default is not None:
            self.value = self.default

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


    def reset(self):
        """
        Initialize the field with its default value and clear all validation messages.
        """
        if self.default is not None:
            self.value = self.default
        else:
            self.value = None
        self.validation_error = ""
            

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

    def handle_typeahead(self, query):
        pass
        # TODO: How to return typeahead data to the caller?


class Form(epflcomponentbase.ComponentContainerBase):
    template_name = "form/form.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts[:]
    js_parts.append("form/form.js")

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
        """
        Make a field known to the parent form. Since any component can reside in a form, the child components 
        which register themselves as fields have to provide the methods reset() and validate() (see :class:`.FormInputBase`),
        since these are called for all registered fields by the parent form.
        """
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
            
    def reset(self):
        """
        Initialize all registered form fields with its default value and clear all validation messages.
        """
        for field in self.registered_fields:
            field.reset()
        self.redraw()

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
