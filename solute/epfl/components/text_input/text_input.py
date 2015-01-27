from solute.epfl.components.form.form import FormInputBase


class TextInput(FormInputBase):
    """
    A form text input.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[TextInput(label="User name:", name="username")])
    
    """
    
    template_name = "text_input/text_input.html"
    
    validation_type = 'text'
