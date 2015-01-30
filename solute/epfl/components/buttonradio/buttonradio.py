from solute.epfl.components.form.form import FormInputBase


class ButtonRadio(FormInputBase):
    """
    A form radio group using buttons as radio fields.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[ButtonRadio(label="Gender:", name="gender", default="male", options=["male", "female"])])

    """

    template_name = "buttonradio/buttonradio.html"
    validation_type = 'text'
    center=False
