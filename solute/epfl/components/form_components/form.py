from solute.epfl.core import epflcomponentbase
from solute.epfl.components import Droppable, Dragable
from odict import odict


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
            result, text = type(
                self.converted_value) is str and len(self.converted_value) > 0, 'Value did not validate as text.'
        elif self.validation_type == 'number':
            result, text = type(
                self.converted_value) is int, 'Value did not validate as number.'
        elif self.validation_type == 'bool':
            result, text = type(
                self.converted_value) is bool, 'Value did not validate as bool.'

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
    template_name = "form_components/form_input.html"

    compo_state = ['name', 'value', 'label', 'input_type', 'validation_error']
    js_parts = "form_components/form_macros.js"
    js_name = ["bootstrap3-typeahead.min.js"]
    css_name = ["form.css"]

    label = None
    name = None
    default = None
    value = None
    input_type = None
    typeahead = False

    def __init__(self, input_type=None, label=None, name=None, typeahead=False, default="", validation_type="",
                 **extra_params):
        super(Input, self).__init__()

    def init_transaction(self):
        if self.value is None and self.default is not None:
            self.value = self.default
        super(Input, self).init_transaction()


def Text(label=None, name=None, default="", typeahead=False, **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='text',
                                                                     validation_type='text',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     typeahead=typeahead,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Number(label=None, name=None, default=0, **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='number',
                                                                     validation_type='number',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Checkbox(label=None, name=None, default=False, mandatory=False, validation_helper=None, **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    if validation_helper is None:
        validation_helper = []
    if mandatory:
        validation_helper.append(
            (lambda x: x.value, 'Mandatory field not checked.'))
    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='checkbox',
                                                                     validation_type='bool',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     validation_helper=validation_helper,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Toggle(label=None, name=None, default=False, on_text="an", off_text="aus", validation_helper=None, **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='toggle',
                                                                     validation_type='bool',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     on_text=on_text,
                                                                     off_text=off_text,
                                                                     css_name=["bootstrap-switch.min.css"],
                                                                     js_name=["bootstrap-switch.min.js"],
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Textarea(label=None, name=None, default="", **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='textarea',
                                                                     validation_type='text',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Select(label=None, name=None, default="", options=[], **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='select',
                                                                     validation_type='text',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     options=options,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Radio(label=None, name=None, default="", options=[], **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='radio',
                                                                     validation_type='text',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     options=options,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


def Buttonradio(label=None, name=None, default="", options=[], **extra_params):
    try:
        structure_params = {'cols': extra_params.pop('cols')}
    except KeyError:
        structure_params = {}

    return epflcomponentbase.ComponentContainerBase(node_list=[Input(input_type='buttonset',
                                                                     validation_type='text',
                                                                     label=label,
                                                                     name=name,
                                                                     default=default,
                                                                     options=options,
                                                                     **extra_params)],
                                                    template_name='form_components/form_label.html',
                                                    label=label,
                                                    **structure_params)


class Button(FormBaseComponent):
    template_name = "form_components/form_button.html"
    js_parts = "form_components/form_button.js"

    label = None
    value = None
    event_name=None
    event_target=None
    is_submit = False

    def __init__(self, label=None, value=None, event_name=None, event_target=None, is_submit=False, **extra_params):
        super(Button, self).__init__()
        if not self.event_name:
            raise Exception('Missing event_name for Button component. %s' % self.cid)
        if not self.event_target:
            self.event_target = self.cid


class MultiSelect_Dragable(Dragable):
    type = "MultiSelect_Dragable"

    def handle_selected(self):
        self.is_selected = True
        self.redraw()

    def handle_unselected(self):
        self.is_selected = False
        self.redraw()


class MultiSelect_Droppable(Droppable):
    valid_types = [MultiSelect_Dragable]


class MultiSelect(epflcomponentbase.ComponentContainerBase, FormBaseComponent):
    template_name = "form_components/form_multiselect.html"
    js_parts = "form_components/form_multiselect.js"

    js_name = ["form.multiselect.js"]

    number_of_selects = 2
    label = None
    value = None
    event_name=None
    event_target=None

    def init_struct(self):
        node_list = []

        # node_list.append(droppable)
        return node_list

    def __init__(self, label=None, value=None, event_name=None, event_target=None, **extra_params):
        super(MultiSelect, self).__init__()
        if "number_of_selects" in extra_params:
            self.number_of_selects = extra_params["number_of_selects"]
        if not self.event_name:
            raise Exception('Missing event_name for MultiSelect component. %s' % self.cid)
        if not self.event_target:
            self.event_target = self.cid

    def init_transaction(self):
        epflcomponentbase.ComponentContainerBase.init_transaction(self)
        for i in range(self.number_of_selects):
            droppable = self.add_component(
                MultiSelect_Droppable(cid=self.cid + "_" + str(i)))

    def add_content(self, selection_index, comp=None, title=None, id=None):
        if comp is None:
            self.components[selection_index].add_component(MultiSelect_Dragable(
                selectable=True, title=title, id=id))
        else:
            # TODO
            raise Exception("Adding existing components is not supported yet!")


    def handle_moveforward(self, select_index):
        from_droppable = self.components[select_index]
        to_droppable = self.components[select_index + 1]
        components_to_move = []
        for comp in from_droppable.components:
            if comp.is_selected == True:
                components_to_move.append(comp)
        # anything > 0 and in increasing order leads to appending elements at
        # the end of to_droppabe
        # TODO: this does not work correctly yet. order in droppable on a epfl.reload_page() may be different. check this.
        pos_counter = 1
        for comp in components_to_move:
            to_droppable.switch_component(
                to_droppable.cid, comp.cid, position=pos_counter)
            comp.is_selected = False
            pos_counter += 1
        if len(components_to_move) > 0:
            from_droppable.redraw()
            to_droppable.redraw()

    def handle_moveback(self, select_index):
        from_droppable = self.components[select_index + 1]
        to_droppable = self.components[select_index]
        components_to_move = []
        for comp in from_droppable.components:
            if comp.is_selected == True:
                components_to_move.append(comp)
        # anything > 0 and in increasing order leads to appending elements at
        # the end of to_droppabe
        # TODO: this does not work correctly yet. order in droppable on a epfl.reload_page() may be different. check this.
        pos_counter = 1
        for comp in components_to_move:
            to_droppable.switch_component(
                to_droppable.cid, comp.cid, position=pos_counter)
            comp.is_selected = False
            pos_counter += 1
        if len(components_to_move) > 0:
            from_droppable.redraw()
            to_droppable.redraw()


class Form(epflcomponentbase.ComponentContainerBase):
    template_name = "form_components/form.html"
    js_parts = "form_components/form.js"

    asset_spec = "solute.epfl.components:form_components/static"

    css_name = ["bootstrap.min.css"]
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
            result.append(field.validate())

        if False in result:
            self.validation_errors = result

        return not False in result

    def get_errors(self):
        return self.validation_errors
