from solute.epfl.components.form.form import FormInputBase


class ButtonRadio(FormInputBase):
    """
    A form radio group using buttons as radio fields.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[ButtonRadio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """
    template_name = "buttonradio/buttonradio.html"
    compo_state = FormInputBase.compo_state + ['options']

    js_parts = FormInputBase.js_parts + ['buttonradio/buttonradio.js']
    js_name = FormInputBase.js_name + [("solute.epfl.components:buttonradio/static", "buttonradio.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:buttonradio/static", "buttonradio.css")]

    options = ""

    validation_type = 'text'
    center=False

