from solute.epfl.components.text_input.text_input import TextInput


class FloatNumberInput(TextInput):
    """
    A form number input that supports float numbers.

    Typically, this component is used in a form:

    .. code:: python

        form = Form(node_list=[FloatNumberInput(label="Distance in meters:", name="distance")])

    """
    
    compo_state = TextInput.compo_state + ['min_value', 'max_value']
    min_value = None #: If set, the minimum value to be supported by the control.
    max_value = None #: If set, the maximum value to be supported by the control.
    
    validation_type = 'float_number'