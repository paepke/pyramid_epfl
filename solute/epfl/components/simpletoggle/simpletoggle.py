from solute.epfl.components.form.form import FormInputBase


class SimpleToggle(FormInputBase):

    """
    A form checkbox styled as a simple on/off toggle.
    Compared to the Toggle component, this component does not display any texts on the toggle.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[SimpleToggle(label="Enable/Disable user:", name="user_enable_toggle")])

    """

    template_name = "simpletoggle/simpletoggle.html"

    validation_type = 'bool'  #: Form validation selector.

    js_name = FormInputBase.js_name + \
        [("solute.epfl.components:simpletoggle/static", "simpletoggle.js")]
    css_name = FormInputBase.css_name + \
        [("solute.epfl.components:simpletoggle/static", "simpletoggle.css")]

    default = False  #: The default value of the toggle.

    js_parts = FormInputBase.js_parts + ['simpletoggle/simpletoggle.js']

    def __init__(self, page, cid,
                 label=None,
                 name=None,
                 value=None,
                 default=False,
                 readonly=False,
                 validation_error='',
                 mandatory=False,
                 fire_change_immediately=False,
                 compo_col=12,
                 label_col=2,
                 layout_vertical=False,
                 label_style=None,
                 input_style=None,
                 **extra_params):
        """
        Form simple toggle Component

        :param label: Optional label describing the input field
        :param name: An element without a name cannot have a value
        :param value: The actual value of the input element that is posted upon form submission
        :param default: Default boolean value that may be pre-set
        :param readonly: Set to true if input cannot be changed and is displayed in readonly mode
        :param validation_error: Set during call of :func:`validate` with an error message if validation fails
        :param mandatory: Set to true if value has to be provided for this element in order to yield a valid form 
        :param fire_change_immediately: Set to true if input change events should be fired immediately to the server. Otherwise, change events are fired upon the next immediate epfl event
        :param compo_col: Set the width of the complete input component (default: max: 12) 
        :param label_col: Set the width of the complete input component (default: 2)
        :param layout_vertical: Set to true if label should be displayed on top of the input and not on the left before it
        :param label_style: Can be used to add additional css styles for the label
        :param input_style: Can be used to add additional css styles for the input
        :param typeahead: Set to true if typeahead should be provided by the input (if supported)
        :param max_length: Maximum length for the input
        :param show_count: Set to true to show a input counter right to the field. Requires a max_length to be set
        :param password: Set to true if input field should be used as a password field
        :param layover_icon: Optional font-awesome icon to be rendered as a layover icon above the input field (aligned to the right)
        """
        super(SimpleToggle, self).__init__(page, cid,
                                           label=label,
                                           name=name,
                                           value=value,
                                           default=default,
                                           readonly=readonly,
                                           validation_error=validation_error,
                                           mandatory=mandatory,
                                           fire_change_immediately=fire_change_immediately,
                                           compo_col=compo_col,
                                           label_col=label_col,
                                           layout_vertical=layout_vertical,
                                           label_style=label_style,
                                           input_style=input_style,
                                           **extra_params)
