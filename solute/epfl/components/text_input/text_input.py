from solute.epfl.components.form.form import FormInputBase


class TextInput(FormInputBase):
    """
    A form text input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[TextInput(label="User name:", name="username")])

    """

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['text_input/text_input.js'])

    js_name = FormInputBase.js_name + [("solute.epfl.components:text_input/static", "text_input.js"),
                                       ("solute.epfl.components:text_input/static", "jquery.datetimepicker.js"),
                                       "bootstrap3-typeahead.min.js"]
    css_name = FormInputBase.css_name + [("solute.epfl.components:text_input/static", "text_input.css"),
                                         ("solute.epfl.components:text_input/static", "jquery.datetimepicker.css")]

    #: Maximum length for the input
    max_length = None

    #: Set True to show a input counter right to the field. Requires a max_length
    show_count = False

    template_name = "text_input/text_input.html"

    validation_type = 'text'

    # : Set to true if typeahead should be provided by the input (if supported)
    typeahead = False

    # : Set the name of the function that is used to generate the typeahead values
    type_func = 'typeahead'

    password = False
    
    #: optional font-awesome icon to be rendered as a layover icon above the input field (aligned to the right)
    layover_icon = None

    date = False

    def handle_typeahead(self, query, compo):
        pass