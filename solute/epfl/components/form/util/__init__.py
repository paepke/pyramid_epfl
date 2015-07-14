from solute.epfl.components import Form
from solute.epfl.components.form.util.validators import ValidatorBase
from solute.epfl.core import epflcomponentbase


class FormInputBase(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:form/static"

    compo_state = ['label', 'name', 'value', 'validation_error', 'readonly', 'mandatory']
    js_parts = ["form/input_base.js"]

    js_name = ["input_base.js"]
    css_name = ["input_base.css"]

    label = None  #: Optional label describing the input field.
    name = None  #: An element without a name cannot have a value.
    value = None  #: The actual value of the input element that is posted upon form submission.
    default = None  #: Default value that may be pre-set or pre-selected
    placeholder = None  #: Placeholder text that can be displayed if supported by the input.
    readonly = False
    #: Set during call of :func:`validate` with an error message if validation fails.
    validation_error = ''
    validation_type = None  #: Form validation selector.
    #: Subclasses can add their own validation helper lamdbas in order to extend validation logic.
    validation_helper = []
    #: Subclasses can add their own ValidatorBase extensions.
    validators = []
    #: Set to true if value has to be provided for this element in order to yield a valid form.
    mandatory = False
    #: If true, underlying form is submitted upon enter key in this input
    submit_form_on_enter = False
    input_focus = False  # : Set focus on this input when component is displayed
    #: Set to true if input change events should be fired immediately to the server.
    #: Otherwise, change events are fired upon the next immediate epfl event.
    fire_change_immediately = False
    compo_col = 12
    label_col = 2
    layout_vertical = False
    label_style = None
    input_style = None

    def __init__(self, page, cid, label=None, name=None, default="", validation_type="",
                 **extra_params):
        super(FormInputBase, self).__init__()

    def is_numeric(self):
        return type(self.value) in [int, float]

    def get_parent_form(self, compo=None):
        if compo is None:
            compo = self.container_compo
        if isinstance(compo, Form):
            return compo
        if not hasattr(compo, 'container_compo'):
            return None
        return self.get_parent_form(compo.container_compo)

    def init_transaction(self):
        super(FormInputBase, self).init_transaction()

        if self.value is None and self.default is not None:
            self.value = self.default


        # try to find a parent form and register this component, but fail silently,
        # since components do not need to be nested inside a form
        try:
            self.get_parent_form(self.container_compo).register_field(self)
        except AttributeError:
            pass

    def delete_component(self):
        try:
            self.get_parent_form(self.container_compo).unregister_field(self)
        except AttributeError:
            pass
        super(FormInputBase, self).delete_component()

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

    def set_focus(self):
        self.add_js_response("setTimeout(function(){$('#%s_input').focus(); }, 0);" % self.cid)
        self.redraw()

    def validate(self):
        """
        Validate the value and return True if it is correct or False if not. Set error messages to self.validation_error
        """
        result, text = True, ''
        if self.validation_type in ['text', 'number', 'float']:
            self.validators.insert(0, ValidatorBase.by_name(self.validation_type)())

        # validation_type bool is always valid

        for helper in self.validation_helper:
            if not result:
                break
            result, text = helper[0](self), helper[1]

        for validator in self.validators:
            if not validator(self):
                result, text = False, validator.error_message

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
            if self.value == None:
                return None
            try:
                return str(self.value)
            except UnicodeEncodeError:
                return unicode(self.value)
        if self.validation_type == 'number':
            if self.value == None:
                return None
            try:
                return int(self.value)
            except ValueError:
                return None
        if self.validation_type == 'bool':
            return bool(self.value)

        if self.validation_type == 'float':
            if self.value == None:
                return None
            try:
                return float(self.value)
            except ValueError:
                return None
        return self.value

    def handle_change(self, value):
        self.value = value

    def __repr__(self):
        return super(FormInputBase, self).__repr__() + str(self.validators)