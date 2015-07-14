from solute.epfl.components.form.util import FormInputBase


class Textarea(FormInputBase):
    """
    A form multi-line text area

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Textarea(label="Provide a description:", name="description")])

    """

    template_name = "textarea/textarea.html"

    validation_type = 'text'

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['textarea/textarea.js'])

    js_name = FormInputBase.js_name + [("solute.epfl.components:textarea/static", "textarea.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:textarea/static", "textarea.css")]


    template_name = "textarea/textarea.html"