# * encoding: utf-8

from solute.epfl.components.text_input.text_input import TextInput


class PasswordInput(TextInput):
    #: Set to true if input field should be used as a password field
    password = True

    def __init__(self, page, cid, password=True, **extra_params):
        """ A Password input this is a convenience component for textinput which overrides the password flag to true,

        :param password: Set to true if input field should be used as a password field
        """
        super(PasswordInput, self).__init__(page, cid, password=password, **extra_params)
