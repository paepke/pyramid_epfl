from solute.epfl.components import cfInput as Input

class PasswordInput(Input):
    """
    A form password input. Compared to other form components, the value of this field is not rendered if the view is reloaded.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[PasswordInput(label="User password:", name="password")])
    
    """
    
    template_name = "password_input/password_input.html"
    
    input_type = 'password'
    validation_type = 'text'
    
    default = '' #: The default value of a password input should always be empty.
    