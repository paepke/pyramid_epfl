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

    js_name = FormInputBase.js_name + [("solute.epfl.components:text_input/static", "text_input.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:text_input/static", "text_input.css")]
    

    template_name = "text_input/text_input.html"
    
    validation_type = 'text'

    password = False