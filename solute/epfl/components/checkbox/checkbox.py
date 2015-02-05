from solute.epfl.components.form.form import FormInputBase


class Checkbox(FormInputBase):
    """
    A form checkbox input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Checkbox(label="I agree to the terms and conditions.", name="toc_agreed")])

    """

    template_name = "checkbox/checkbox.html"

    validation_type = 'bool'
    validation_helper = FormInputBase.validation_helper[:]
    validation_helper.append(
        (lambda x: ((not x.mandatory) or x.value), 'Mandatory field not checked.'))
