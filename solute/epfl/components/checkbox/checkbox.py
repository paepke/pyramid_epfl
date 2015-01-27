from solute.epfl.components.form.form import FormInputBase


class Checkbox(FormInputBase):

    template_name = "checkbox/checkbox.html"

    validation_type = 'bool'
    validation_helper = FormInputBase.validation_helper[:]
    validation_helper.append(
        (lambda x: ((not x.mandatory) or x.value), 'Mandatory field not checked.'))
