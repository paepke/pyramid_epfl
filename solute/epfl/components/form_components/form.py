from solute.epfl.core import epflcomponentbase


class Input(epflcomponentbase.ComponentBase):
    template_name = "form_components/form.input.html"

    label = None
    name = None
    value = None
    link = None

    @staticmethod
    def format_helper(type_helper, input_type, label=None, name=None, link=None, value="", extra_params=None):
        if extra_params is None:
            extra_params = {}
        params = {'input_type': input_type,
                  'name': name,
                  'label': label,
                  'value': value,
                  'link': link}
        params.update(extra_params)
        return (Input,
                params)


class Button(epflcomponentbase.ComponentBase):
    template_name = "form_components/form.button.html"
    label = None
    value = None
    callback = None

    @staticmethod
    def format_helper(type_helper, label=None, value=None, callback=None, extra_params=None):
        if extra_params is None:
            extra_params = {}
        params = {'label': label,
                  'value': value,
                  'callback': callback}
        params.update(extra_params)
        return (Button,
                params)


class TypeHelper(object):
    Input = Input.format_helper
    Button = Button.format_helper


class Form(epflcomponentbase.ComponentTreeBase):
    template_name = "form_components/form.html"
    asset_spec = "solute.epfl.components:form_components/static"

    css_name = ["bootstrap.min.css"]

    type_helper = TypeHelper()

    fields = []

    def __init__(self, **config):
        super(Form, self).__init__(**config)

    def init_form_fields(self):
        return []

    def init_tree_struct(self):
        self.node_list = self.init_form_fields()

        for field in self.fields:
            field_type, args, kwargs = field
            print args, kwargs
            self.node_list.append(getattr(self.type_helper, field_type)(*args, **kwargs))
