from solute.epfl.components.form.form import FormInputBase


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
    
    options = [] #: A list if options for the select input.
    
    compo_state = FormInputBase.compo_state + ['options']

    validation_type = 'text'
    layout_vertical = False
