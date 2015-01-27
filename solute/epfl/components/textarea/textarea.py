from solute.epfl.components import cfInput as Input

class Textarea(Input):
    """
    A form multi-line text area
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[Textarea(label="Provide a description:", name="description")])
    
    """
    

    validation_type = 'text'
    input_type = 'textarea'
