from solute.epfl.components.form.form import FormInputBase


class NumberInput(FormInputBase):
    
    template_name = "number_input/number_input.html"
    
    validation_type = 'number'