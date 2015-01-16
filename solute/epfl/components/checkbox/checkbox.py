from solute.epfl.components import cfInput as Input

class Checkbox(Input):
    input_type = 'checkbox'
    validation_type = 'bool'
    validation_helper = Input.validation_helper[:]
    validation_helper.append(
        (lambda x: ((not x.mandatory) or x.value), 'Mandatory field not checked.'))