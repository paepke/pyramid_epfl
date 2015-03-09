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

    #: If set to True, label and checkbox are not splitted to different bootstrap rows,
    # but placed directly next to each other.
    compact = False

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['checkbox/checkbox.js'])
    js_name = FormInputBase.js_name + [("solute.epfl.components:checkbox/static", "checkbox.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:checkbox/static", "checkbox.css")]

