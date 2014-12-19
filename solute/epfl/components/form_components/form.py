from solute.epfl.core import epflcomponentbase


class FormBaseComponent(epflcomponentbase.ComponentBase):
    asset_spec = "solute.epfl.components:form_components/static"

    compo_state = ['name', 'value', 'validation_error']

    # An element without a name can not have a value.
    name = None
    value = None
    validation_error = ''
    validation_type = None
    validation_helper = []

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

        result, text = False, ''
        if self.validation_type == 'text':
            result, text = type(self.converted_value) is str, 'Value did not validate as text.'
        elif self.validation_type == 'number':
            result, text = type(self.converted_value) is int, 'Value did not validate as number.'
        elif self.validation_type == 'bool':
            result, text = type(self.converted_value) is bool, 'Value did not validate as bool.'

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


class Input(FormBaseComponent):
    template_name = "form_components/form.input.html"

    compo_state = ['name', 'value', 'label', 'input_type', 'validation_error']

    label = None
    name = None
    default = None
    value = None
    input_type = None

    def __init__(self, input_type=None, label=None, name=None, default="", validation_type="", **extra_params):
        self.value = self.default
        super(Input, self).__init__()


def Text(label=None, name=None, default="", **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='text',
                                                                validation_type='text',
                                                                label=label,
                                                                name=name,
                                                                default=default,
                                                                **extra_params)],
                                               template_name='form_components/form.label.html',
                                               label=label)


def Number(label=None, name=None, default=0, **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='number',
                                                                validation_type='number',
                                                                label=label,
                                                                name=name,
                                                                default=default,
                                                                **extra_params)],
                                               template_name='form_components/form.label.html',
                                               label=label)


def Checkbox(label=None, name=None, default=False, mandatory=False, validation_helper=None, **extra_params):
    if validation_helper is None:
        validation_helper = []
    if mandatory:
        validation_helper.append((lambda x: x.value, 'Mandatory field not checked.'))
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='checkbox',
                                                                validation_type='bool',
                                                                label=label,
                                                                name=name,
                                                                default=default,
                                                                validation_helper=validation_helper,
                                                                **extra_params)],
                                               template_name='form_components/form.label.html',
                                               label=label)

def Toggle(label=None, name=None, default=False, on_text="an", off_text="aus", validation_helper=None, **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='toggle',
                                                                validation_type='bool',
                                                                label=label,
                                                                name=name,
                                                                default=default,
                                                                on_text=on_text,
                                                                off_text=off_text,
                                                                css_name=["bootstrap-switch.min.css"],
                                                                js_name=["bootstrap-switch.min.js"],
                                                                **extra_params)],
                                               template_name='form_components/form.label.html',
                                               label=label)


def Textarea(label=None, name=None, default="", **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='textarea',
                                                                validation_type='text',
                                                                label=label,
                                                                name=name,
                                                                default=default,
                                                                **extra_params)],
                                               template_name='form_components/form.label.html',
                                               label=label)

def Select(label=None, name=None, default="",options=[], **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='select',
                                                            validation_type='text',
                                                            label=label,
                                                            name=name,
                                                            default=default,
                                                            options=options,
                                                            **extra_params)],
                                           template_name='form_components/form.label.html',
                                           label=label)

def Radio(label=None, name=None, default="",options=[], **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='radio',
                                                            validation_type='text',
                                                            label=label,
                                                            name=name,
                                                            default=default,
                                                            options=options,
                                                            **extra_params)],
                                           template_name='form_components/form.label.html',
                                           label=label)

def Buttonset(label=None, name=None, default="",options=[], **extra_params):
    return epflcomponentbase.ComponentTreeBase(node_list=[Input(input_type='buttonset',
                                                            validation_type='text',
                                                            label=label,
                                                            name=name,
                                                            default=default,
                                                            options=options,
                                                            **extra_params)],
                                           template_name='form_components/form.label.html',
                                           label=label)


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

    def __init__(self, node_list=None, validate_hidden_fields=False, **extra_params):
        super(Form, self).__init__()

    def register_field(self, field):
        self._registered_fields.append(field.cid)

    @property
    def registered_fields(self):
        return [self.page.components[cid] for cid in self._registered_fields]

    def get_values(self):
        values = []
        for field in self.registered_fields:
            if field.name is None:
                continue
            values.append((field.name, field.converted_value))
        return values

    def validate(self):
        result = []
        for field in self.registered_fields[:]:
            # Do not validate fields without a name, cause they can not contain a value.
            if field.name is None:
                continue
            if not self.validate_hidden_fields and not field.is_visible():
                continue
            result.append(field.validate())
        return not False in result, result