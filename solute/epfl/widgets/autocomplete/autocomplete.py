# -*- coding: utf-8 -*-

from solute.epfl import json

from solute.epfl.core import epflwidgetbase
from solute.epfl.core import epflfieldbase

from wtforms import validators

# todo:
# to inverse to "get_data": "get_entry": needed, if you use set_data to set the data and want to show automatically the displayed entry



class AutocompleteWidget(epflwidgetbase.WidgetBase):

    """ Displays a normal text-entry with autocomplete feature.
    """

    name = "autocomplete"
    template_name = "autocomplete/autocomplete.html"
    asset_spec = "solute.epfl.widgets:autocomplete/static"

    js_name = ["autocomplete.js"]
    css_name = ["autocomplete.css"]

    param_def = {"on_change": epflwidgetbase.EventType,
                 "get_data": epflwidgetbase.MethodType,        # the function that gets the current input as parameter and
                                                               # returns the matching possible values (list of tuples (value, visual))

                 "match_required": (epflwidgetbase.BooleanType, False), # if true, the entered value must be from the "get_data"-method, so
                                                                        # this ensures that the value is from the defined domain, but
                                                                        # you can not "create" new values
                 }

    input_type = "Text"

    def update_data_source(self, data_source):
        widget_name = data_source.name

        style = data_source.kwargs.get('style', '')
        data_source.style = style

        class_ = data_source.kwargs.get('class_', '')
        data_source.class_ = class_

        data_source.entry_data = self.state["entry_data"]



    def handle_GetData(self, query):
        domain = self.params["get_data"](query)
        self.form.return_ajax_response(domain)



    def handle_ValueChange(self, value):

        self.field.process_formdata([value["value"]])
        self.field.set_entry_data(value["entry"])






class AutoComplete(epflfieldbase.FieldBase):

    widget_class = AutocompleteWidget

    def init_state(self):
        super(AutoComplete, self).init_state()

        self.set_entry_data("")

    def setup_state(self):
        super(AutoComplete, self).setup_state()

    def setup_validators(self):
        super(AutoComplete, self).setup_validators()

        # remove the DataRequired-Validator because it is not compatible with the
        # autocomplete logic (self.data only contains matched values)
        for validator in self.validators[:]:
            if isinstance(validator, validators.DataRequired):
                self.validators.remove(validator)

        if self.widget.params["match_required"]:
            self.validators.append(MatchRequired())

        if self.state["mandatory"]:
            # madatory only means that something is entered into the field
            # not neccessary a "valid" value
            self.validators.append(EntryDataRequired())



    def set_entry_data(self, data):
        """ This is the data which is displayed/entered into the actual autocomplete-field.
        Whereas the self.data is the corresponding "value".
        For example: You type in the name of a category and the self.data is then the corresponding
        category-id. Of course the self.data may be None if nothing matching is found in the
        data returned by the "get_data"-function.
        """
        self.state["entry_data"] = data



class MatchRequired(object):

    field_flags = ('required', )
    visual = "*"

    def __init__(self, message = "txt_autocomplete_match_required"):
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            # data only contains valid choices...
            field.errors[:] = []
            raise validators.StopValidation(self.message)


class EntryDataRequired(object):

    field_flags = ('required', )
    visual = "*"

    def __init__(self, message = "txt_required_field"):
        self.message = message

    def __call__(self, form, field):
        # talking about the entry_data-field here
        entry_data = field.state["entry_data"]
        if not entry_data or not entry_data.strip():
            field.errors[:] = []
            raise validators.StopValidation(self.message)



