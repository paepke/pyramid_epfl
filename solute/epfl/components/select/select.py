from solute.epfl.components.form.form import FormInputBase


class Select(FormInputBase):

    template_name = "select/select.html"

    validation_type = 'text'
