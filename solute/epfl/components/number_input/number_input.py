from solute.epfl.components.form.form import FormInputBase


class NumberInput(FormInputBase):
    """
    A form number input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[NumberInput(label="Age:", name="age")])

    """
    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['number_input/number_input.js'])
    js_name = FormInputBase.js_name + [("solute.epfl.components:number_input/static", "number_input.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:number_input/static", "number_input.css")]

    template_name = "number_input/number_input.html"
    compo_state = FormInputBase.compo_state + ['min_value', 'max_value']

    validation_type = 'number'#:float or number
    layout_vertical = False
    min_value = None #: If set, the minimum value to be supported by the control.
    max_value = None #: If set, the maximum value to be supported by the control.