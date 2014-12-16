from solute.epfl.core import epflcomponentbase


class Input(epflcomponentbase.ComponentBase):
    template_name = "form_components/form.input.html"
    asset_spec = "solute.epfl.components:form_components/static"

    label = None
    name = None
    value = None
    link = None
    input_type = None

    def __init__(self, input_type=None, label=None, name=None, link=None, value="", **extra_params):
        super(Input, self).__init__()


class Button(epflcomponentbase.ComponentBase):
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

    fields = []

    def __init__(self, fields=None, **extra_params):
        super(Form, self).__init__()

    def init_tree_struct(self):
        return self.fields


class Types(object):
    Form = Form
    Button = Button
    Input = Input