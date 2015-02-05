from solute.epfl.components.form.form import FormInputBase


class Textarea(FormInputBase):
    """
    A form multi-line text area
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[Textarea(label="Provide a description:", name="description")])
    
    """
    
    template_name = "textarea/textarea.html"

    validation_type = 'text'
