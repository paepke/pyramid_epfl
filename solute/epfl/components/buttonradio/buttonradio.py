from solute.epfl.components import cfInput as Input

class ButtonRadio(Input):
    
    """
    A form radio group using buttons as radio fields.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[ButtonRadio(label="Gender:", name="gender", default="male", options=["male", "female"])])
    
    """

    validation_type = 'text'
    input_type = 'buttonset'
