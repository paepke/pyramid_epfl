from solute.epfl.components.form.util import FormInputBase


class Select(FormInputBase):
    """
    A form drop-down select input.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[Select(label="Select color:",
                                      name="color",
                                      default="black",
                                      options=[{"value":"white","visual":"White"},{"value":"red","visual":"Red"},{"value":"black","visual":"Black"}])])

    """

    template_name = "select/select.html"
    
    options = None #: A list if options for the select input.
    
    compo_state = FormInputBase.compo_state + ['options']

    validation_type = 'text'
    layout_vertical = False

    js_parts = FormInputBase.js_parts[:]
    js_parts.extend(['select/select.js'])
    js_name = FormInputBase.js_name + [("solute.epfl.components:select/static", "select.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:select/static", "select.css")]

    validation_type = 'text'