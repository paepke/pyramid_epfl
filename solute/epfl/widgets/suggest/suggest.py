# -*- coding: utf-8 -*-

from solute.epfl import json

from solute.epfl.core import epflwidgetbase
from solute.epfl.core import epflfieldbase
from wtforms import validators

# todo:
# to inverse to "get_data": "get_entry": needed, if you use set_data to set the data and want to show automatically the displayed entry



class SuggestWidget(epflwidgetbase.WidgetBase):

    """ Displays a normal text-entry with autocomplete feature.
    """

    name = "suggest"
    template_name = "suggest/suggest.html"
    asset_spec = "solute.epfl.widgets:suggest/static"

    js_name = ["suggest.js"]
    css_name = ["suggest.css"]

    param_def = {"on_change": epflwidgetbase.EventType,
                 "get_data": epflwidgetbase.MethodType,        # the function that gets the current input as parameter and
                                                               # returns the matching possible values (list of tuples [(value, visual), ...])
                                                               # This function must filter its results accordingly to the given input!

                 "match_required": (epflwidgetbase.BooleanType, False), # if true, the entered value must be from the "get_data"-method, so
                                                                        # this ensures that the value is from the defined domain, but
                                                                        # you can not "create" new values

                 "new_value_func": epflwidgetbase.OptionalMethodType, # this function is called, with the string entered into the field
                                                                      # when "match_required" is false and the user
                                                                      # enters a visual, that is not available in the list of possible values
                                                                      # (returned by "get_data")
                                                                      # The method MUST raise an ValueError with some error-message
                                                                      # or return the new "value" for the given "visual" if it could not
                                                                      # create the new value!
                 }

    input_type = "Text"

    def update_data_source(self, data_source):
        widget_name = data_source.name

        style = data_source.kwargs.get('style', '')
        data_source.style = style

        class_ = data_source.kwargs.get('class_', '')
        data_source.css_classes.append(class_)

        data_source.entry_data = self.state["entry_data"]



    def handle_GetData(self, query):
        domain = self.params["get_data"](query)
        self.form.return_ajax_response(domain)



    def handle_ValueChange(self, value):

        self.field.process_formdata([value["value"]])
        self.field.set_entry_data(value["entry"])


class Suggest(epflfieldbase.FieldBase):

    widget_class = SuggestWidget

    def init_state(self):
        super(Suggest, self).init_state()

        self.set_entry_data("")

    def setup_state(self):
        super(Suggest, self).setup_state()

    def create_new_value(self):
        """ Called if form.validate was called with create_new_values=True for every field.
        Here a field (e.g. Suggest) can check, if a new value must be created by the application-model
        that the field can be validated correctly.
        """
        entry_data = self.state["entry_data"] # this is the visual the user typed into the field

        if entry_data:
            entry_data = entry_data.strip()

        if entry_data and not self.data:
            # so, we have user-typed-in-data but no match to the model in self.data!
            new_value_func = self.widget.params["new_value_func"]
            if new_value_func:
                try:
                    new_value = new_value_func(entry_data)
                except ValueError, e:
                    msg = self.gettext(e.message)
                    self.process_errors.append(msg) # this has to go here (self.process_errors), because the
                                                    # following self.validate will empty self.errors and
                                                    # overwrite it with the contents of self.process_errors
                    return

                self.data = new_value # directly use the newly created value

    def setup_validators(self):
        super(Suggest, self).setup_validators()

        # remove the DataRequired-Validator because it is not compatible with the
        # autocomplete logic (self.data only contains matched values)
        for validator in self.validators[:]:
            if isinstance(validator, validators.DataRequired) or isinstance(validator, epflfieldbase.FieldMandatory):
                self.validators.remove(validator)

        if self.widget.params["match_required"]:
            self.validators.append(MatchRequired())

        elif self.state["mandatory"]:
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

    def __init__(self, message = "txt_value_required"):
        self.message = message

    def __call__(self, form, field):
        # talking about the entry_data-field here
        entry_data = field.state["entry_data"]
        if not entry_data or not entry_data.strip():
            field.errors[:] = []
            message = field.gettext(self.message)
            raise validators.StopValidation(message)



