from solute.epfl.core import epflcomponentbase
from solute.epfl.components import Droppable, Dragable
from collections2 import OrderedDict as odict


class FormInputBase(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:form/static"

    compo_state = ['label', 'name', 'value', 'validation_error', 'readonly']
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
    validation_type = None
    #: Subclasses can add their own validation helper lamdbas in order to extend validation logic.
    validation_helper = []
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

    def init_transaction(self):
        super(FormInputBase, self).init_transaction()

        if self.value is None and self.default is not None:
            self.value = self.default

        def get_parent_form(compo):
            if isinstance(compo, Form):
                return compo
            if not hasattr(compo, 'container_compo'):
                return None
            return get_parent_form(compo.container_compo)

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
        
    def set_focus(self):
        self.add_js_response("setTimeout(function(){$('#%s_input').focus(); }, 0);" % self.cid)
        self.redraw()
        
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
                if ((not self.min_value is None) and (int(self.value)<self.min_value)):
                    result, text = False, ('Value must not be lower than %s.' % self.min_value)
                elif ((not self.max_value is None) and (int(self.value)>self.max_value)):
                    result, text = False, ('Value must not be higher than %s.' % self.max_value)
        elif self.validation_type == 'float':
            if self.mandatory and ((self.value is None) or (self.value == "")):
                result, text = False, 'Value is required'
            elif ((not self.value is None) and (self.value != "")):
                try:
                    float(self.value)
                except ValueError:
                    result, text = False, 'Value did not validate as number.'
                if ((not self.min_value is None) and (int(self.value)<self.min_value)):
                    result, text = False, ('Value must not be lower than %s.' % self.min_value)
                elif ((not self.max_value is None) and (int(self.value)>self.max_value)):
                    result, text = False, ('Value must not be higher than %s.' % self.max_value)
                    
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


class Form(epflcomponentbase.ComponentContainerBase):
    template_name = "form/form.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts[:]
    js_parts.append("form/form.js")

    asset_spec = "solute.epfl.components:form/static"
    js_name = ["form.js"]

    compo_state = ["_registered_fields", "is_dirty"]

    fields = []
    _registered_fields = None
    validation_errors = None
    _registered_fields = None
    validation_errors = []

    validate_hidden_fields = False
    is_dirty = False

    def __init__(self, page, cid, node_list=None, validate_hidden_fields=False, **extra_params):
        super(Form, self).__init__()

    def handle_submit(self):
        pass
    
    def handle_set_dirty(self):
        self.is_dirty = True

    def register_field(self, field):
        """
        Make a field known to the parent form. Since any component can reside in a form, the child components 
        which register themselves as fields have to provide the methods reset() and validate() (see :class:`.FormInputBase`),
        since these are called for all registered fields by the parent form.
        """
        if self._registered_fields is None:
            self._registered_fields = []
        self._registered_fields.append(field.cid)

    @property
    def registered_fields(self):
        return [self.page.components[cid] for cid in self._registered_fields]

    @property
    def registered_names(self):
        return dict([[self.page.components[cid].name, self.page.components[cid]]
                     for cid in self._registered_fields
                     if hasattr(self.page.components[cid], 'name') and self.page.components[cid].name is not None])

    def get_values(self):
        values = odict()
        print "get_values",self.registered_fields

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
