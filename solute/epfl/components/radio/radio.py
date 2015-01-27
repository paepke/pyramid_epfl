from solute.epfl.components import cfInput as Input

class Radio(Input):
    """
    A form radio group.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[Radio(label="Gender:", name="gender", default="male", options=["male", "female"])])
    
    """

    validation_type = 'text'
    input_type = 'radio'
