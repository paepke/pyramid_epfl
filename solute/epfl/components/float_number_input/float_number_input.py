from solute.epfl.components.text_input.text_input import TextInput

def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

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
    
    validation_helper = TextInput.validation_helper[:]
    validation_helper.append(
        (lambda x: (is_float(x.value)), 'Value did not validate as number.'))
    validation_helper.append(
        (lambda x: ((x.min_value is None) or (float(x.value)<x.min_value)), 'Value must not be lower than the min value.'))
    validation_helper.append(
        (lambda x: ((x.max_value is None) or (float(x.value)>x.max_value)), 'Value must not be higher than the max value.'))