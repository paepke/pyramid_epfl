from solute.epfl.components.form.form import FormInputBase


class Radio(FormInputBase):
    """
    A form radio group.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Radio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """

    template_name = "radio/radio.html"

    validation_type = 'text'
