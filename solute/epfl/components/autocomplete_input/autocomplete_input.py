# * encoding: utf-8

from solute.epfl.components.text_input.text_input import TextInput


class AutoCompleteInput(TextInput):
    #: Set to true if typeahead should be provided by the input (if supported)
    typeahead = True

    #: Set the name of the function that is used to generate the typeahead values
    type_func = 'typeahead'

    def __init__(self, page, cid, typeahead=True, **extra_params):
        """AutoComplete Input this is a convenience component for textinput which overrides the typeahead flag to true,

        :param typeahead: Set to true if typeahead should be provided by the input (if supported)
        """
        super(AutoCompleteInput, self).__init__(page, cid, typeahead=typeahead, **extra_params)

    def handle_typeahead(self, query):
        """Override Me
        :param query: the text typed in input
        """
        pass