from solute.epfl.components.form.form import FormBaseComponent

class Input(FormBaseComponent):
    template_name = "input/input.html"

    compo_state = FormBaseComponent.compo_state + ['label', 'input_type']
    js_parts = FormBaseComponent.js_parts + ["input/input.js"]
        
    js_name = FormBaseComponent.js_name + [("solute.epfl.components:input/static", "input.js"), ("solute.epfl.components:input/static", "bootstrap3-typeahead.min.js")]
    css_name = FormBaseComponent.css_name + [("solute.epfl.components:input/static", "input.css")]

    label = None
    name = None
    default = None
    placeholder = None
    value = None
    input_type = None
    mandatory = False #: True if input field is mandatory
    typeahead = False #: True if typeahead is supported 
    submit_form_on_enter = False #: If true, underlying form is submitted upon enter key in this input 
    input_focus = False #: Set focus on this input when component is displayed

    def __init__(self, input_type=None, label=None, name=None, typeahead=False, default="", validation_type="",
                 **extra_params):
        super(Input, self).__init__()

    def init_transaction(self):
        if self.value is None and self.default is not None:
            self.value = self.default
        super(Input, self).init_transaction()
        
    def handle_typeahead(self, query):
        pass
        # TODO: How to return typeahead data to the caller?
