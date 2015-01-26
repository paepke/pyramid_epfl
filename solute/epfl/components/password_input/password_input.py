from solute.epfl.components import cfInput as Input

class PasswordInput(Input):
    input_type = 'password'
    validation_type = 'text'
    default = ''
    
    @property
    def converted_value(self):
        pw_value = self.value
        # clear stored value
        self.value = ""
        return pw_value