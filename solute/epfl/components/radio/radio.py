from solute.epfl.components.form.form import FormInputBase


class Radio(FormInputBase):
    """
    A form radio group.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Radio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """

    options = ""

    compo_state = FormInputBase.compo_state + ['options']

    template_name = "radio/radio.html"

    validation_type = 'text'

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['radio/radio.js'])

    js_name = FormInputBase.js_name + [("solute.epfl.components:radio/static", "radio.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:radio/static", "radio.css")]