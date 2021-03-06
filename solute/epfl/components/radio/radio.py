from solute.epfl.components.form.inputbase import FormInputBase


class Radio(FormInputBase):
    """
    A form radio group.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Radio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """
    template_name = "radio/radio.html"

    js_name = FormInputBase.js_name + [("solute.epfl.components:radio/static", "radio.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:radio/static", "radio.css")]

    js_parts = FormInputBase.js_parts + ['radio/radio.js']

    compo_state = FormInputBase.compo_state + ['options']

    validation_type = 'text'  #: Validate as a text.
    options = None  #: List of strings or key, value tuples to be used as options.

    def __init__(self, page, cid, options=None, **extra_params):
        """Simple radio form component.

        :param options: List of strings or key, value tuples to be used as options.
        """
        super(Radio, self).__init__(page, cid, **extra_params)
