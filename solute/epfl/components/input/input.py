from solute.epfl.components.form.form import FormBaseComponent

class Input(FormBaseComponent):
    template_name = "input/input.html"

    compo_state = FormBaseComponent.compo_state[:]
    compo_state.extend(['label', 'input_type'])
    js_parts = "input/input.js"
    js_name = ["bootstrap3-typeahead.min.js"]
    css_name = ["form.css"]

    label = None
    name = None
    default = None
    placeholder = None
    value = None
    input_type = None
    mandatory = False
    typeahead = False

    def __init__(self, input_type=None, label=None, name=None, typeahead=False, default="", validation_type="",
                 **extra_params):
        super(Input, self).__init__()

    def init_transaction(self):
        if self.value is None and self.default is not None:
            self.value = self.default
        super(Input, self).init_transaction()
