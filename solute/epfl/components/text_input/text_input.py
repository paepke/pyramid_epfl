from solute.epfl.components import cfInput as Input

class TextInput(Input):
    """
    A form text input.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[TextInput(label="User name:", name="username")])
    
    """
    
    input_type = 'text'
    validation_type = 'text'
