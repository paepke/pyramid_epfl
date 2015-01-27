from solute.epfl.components.form.form import FormInputBase


class NumberInput(FormInputBase):
    """
    A form number input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[NumberInput(label="Age:", name="age")])

    """
    
    template_name = "number_input/number_input.html"
    
    validation_type = 'number'