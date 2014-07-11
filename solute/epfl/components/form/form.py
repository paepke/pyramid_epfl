# coding: utf-8

"""
A web-form component based on WTForms.

The python part

"""

from pprint import pprint

import types, os.path, string
from datetime import datetime

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflfieldbase
from solute.epfl.core import epfltransaction
from solute.epfl.core import epflconfig
from solute.epfl.core import epfll10n

import jinja2
import wtforms


NO_DEFAULT = lambda x:x # an atom


class Form(epflcomponentbase.ComponentBase, wtforms.Form):
    """ This is a mixture of a WTForms-Form and a epfl-base-component """

    template_name = "form/form.html"
    asset_spec = "solute.epfl.components:form/static"

    css_name = ["form.css"]
    js_name = ["form.js",
               "epflwidgetbase.js"]

    compo_state = ["field_state", "form_data_store", "additional_data"]

    field_state = {}
    form_data_store = {}
    additional_data = {}

    class Meta(object):
        def get_translations(self, form):
            return epfll10n.BasicDB()



    def __init__(self):

        self.raw_data = None
        self.submit_button_name = None # name of the current submit-button which submitted this form

        # this part is to init the wtforms-super-class
        # the original is not usable, because it tries to process the formdata (normally coming from query-params).
        # these are not available here, also the component is not set up at this time to survive a call to "process"
        # so this is left out here!
        meta_obj = self._wtforms_meta()
        super(wtforms.Form, self).__init__(self._unbound_fields, meta=meta_obj, prefix="")

        for name, field in wtforms.compat.iteritems(self._fields):
            # Set all the fields to attributes so that they obscure the class
            # attributes with the same names.
            setattr(self, name, field)

        # finally init the epfl-part
        epflcomponentbase.ComponentBase.__init__(self)


        self.action = ""
        self.target_widget = None # the widget that received the last cmd


    def get_field_state(self, field_name):
        """ Returns and creates the state for a field and widget. This is called during the binding of a field and its widget to the form.
        This state is shared between field and widget.
        """

        if field_name not in self.field_state:
            self.field_state[field_name] = {}

        return self.field_state[field_name]


    def setup_component_state(self):
        """ Setup of the widget-states and the form-state """

        super(Form, self).setup_component_state()

        # late-init of wtform
        formdata = FormDataProvider(self.page_request, self.form_data_store, self.page.transaction)

        for field in self:
            if field.widget:
                if isinstance(field, epflfieldbase.FieldBase):
                    field.widget.setup_state()
                    field.setup_state()
                else:
                    raise TypeError, "only EPFL-Fields are supported: " + repr(field)

        self.process(formdata)

    def finalize_component_state(self):

        for field in self:
            if field.widget:
                field.widget.finalize_state()
                field.finalize_state()

        # write back the field-data into the transaction
        for field in self:
            self.form_data_store[field.name] = field.data

        super(Form, self).finalize_component_state()

    def validate(self, create_new_values = False):
        """
        Additionally to the validation (done by the original-wtforms-class) it can create new values.
        This will be done if create_new_values = True:
        New values occur e.g. as the value-visuals the user types in at SuggestWidgets that have
        match_required=False and a new_value_func defined.
        When some data was typed in that is not in the list the SuggestWidget's get_data-function returned,
        the new_value_func is called with the new value.
        """

        if create_new_values:
            for field in self:
                field.create_new_value()

        return super(Form, self).validate()


    def get_data(self, key = None, default = NO_DEFAULT, validate = False):
        """ Returns all values of this form as a dictionary.
        Or if "key" is given, only that value is returned.
        This is the way to get only one additional_data-key back!
        "default" only works in combination with "key"
        """

        if validate:
            if not self.validate():
                return None

        if key is None:
            data = self.data.copy()
            data.update(self.additional_data)
            return data
        else:
            if key in self.additional_data:
                return self.additional_data[key]
            elif key in self:
                return self[key].data
            elif default is not NO_DEFAULT:
                return default
            else:
                raise KeyError, key

    def set_data(self, data):
        """ Sets multiple values of this form by passing a dictionary/dicionary like/object with attributes.
        Values not defined as attributes of the form are stored separately and returned unchanged by self.get_data().
        Also the self.after_form_set_data of all fields will be triggered!
        """

        if hasattr(data, "items"): # works for dict-like objects
            for field_name, field_value in data.items():
                if field_name in self:
                    self[field_name].data = field_value
                else:
                    self.additional_data[field_name] = field_value

        if hasattr(data, field_name): # works for attributes of objects
            if field_name in self.data.keys():
                self[field_name].data = getattr(data, field_name)
            else:
                self.additional_data[field_name] = field_value

        for field in self:
            field.after_form_set_data() # a convenience-hook

    def get_errors(self):
        """ Returns the errors from all fields """
        errors = {}
        for field in self:
            errors[field.name] = field.errors
        return errors


    def reset_data(self, tag = None, additional_data = False):
        """ Sets the data of the form to the default values.
        If additional_data == True: remove all aditional_data """

        if additional_data:
            self.additional_data = {}

        if tag:
            items = self.get_fields_by_tag(tag)
        else:
            items = self

        for field in items:
            field.reset_data()


    def do_get(self):
        """ Called for all HTTP-GET-Requests - overwrite to read data into the form """
        pass

    def do_post(self):
        """ Called for all HTTP-POST-Requests - overwrite to write data into the database """
        pass


    def set_component_id(self, cid):
        """ Tells the form its component-id. The component-id is the name of the attribute of the page object to which
        the component was assined.
        This function is called by the __setattr__-function of the page-object
        """

        # erst mal für mich selbst...
        epflcomponentbase.ComponentBase.set_component_id(self, cid)

        # ...und nun an alle widgets die es interessiert durchpropagieren
        for field in self:
            field.form_obj = self

    def which_submit_button(self, name):
        """ Returns True, if the form was submitted by a button called 'name'.
        This test is usefull if you have a form with two or more submit-buttons.
        """

        if not self.raw_data:
            return False

        # this check is valid for all field types...
        if "__submitting_element_id__" in self.raw_data:
            # if we got submitted by "submit_form()"-js of a form-component
            # we know the name this is often the case for on_change-submits
            return self.raw_data["__submitting_element_id__"] == name

        # the following checks are valid for buttons only...
        field = getattr(self, name)
        if not isinstance(field, wtforms.SubmitField):
            return False

        if name in self.raw_data:
            return True # simplest case

        if name + ".x" in self.raw_data:
            return True # the button was type "image"

        return False


    def get_submit_handler(self, params):
        """ Returns the submit-handler-function for this full-page-call """

        for attr_name in self.__class__.__dict__:
            if attr_name.startswith("submit_"):
                func = getattr(self, attr_name)
                if type(func) is types.MethodType:

                    # this submit_*-function exists, so check if this button was pressed
                    # ... since we can not look into the template thats all we can do to
                    # determine the possible button-names
                    if self.which_submit_button(attr_name[7:]):
                        self.submit_button_name = attr_name[7:]
                        return func

        return None


    def handle_submit(self, params):
        """
        Called by the system (epflpage.Page.handle_submit_request) with the CGI-params once for every non-ajax-request
        Checks if the submit was from this form and calls the corresponding submit_*-handler.
        """

        submit_handler = self.get_submit_handler(params)


        if submit_handler:
            submit_handler()

    def get_submit_button(self):
        """ You can call this in the do_get or do_post methods to check, if the form-submission was by a submit-button.
        """
        return self.submit_button_name


    def pre_render(self):
        """ Called just before jina-rendering occures. """

        epflcomponentbase.ComponentBase.pre_render(self)

        # for epfl-widgets
        for field in self:
            if field.widget:
                field.widget.pre_render()

    def render(self, *args, **kwargs):

        return super(Form, self).render(*args, **kwargs)

    def _get_template_element(self, part_accessor):
        if len(part_accessor) > 0 and part_accessor[0] == "macros":
            return None # macros are not template-elements
        elif len(part_accessor) == 1: # this is very static, but lets start simple!
            return getattr(self, part_accessor[0], None)
        else:
            return None



    def get_js_part(self):
        """ gets the javascript-portion of the component """
        form_js = [super(Form, self).get_js_part()]

        for field in self:
            js_part = field.widget.get_js_part()
            if js_part:
                form_js.append(js_part)
##            if field.description:
##                form_js.append(self.js_call("this.add_tooltip", field.name, field.description))

        return "".join(form_js)

    def get_fields_by_type(self, typ):
        """ Returns a list of all buttons or fields, depending on the type "typ" """

        out = []

        if typ == "button":
            return [field for field in self if field.widget.name == "button"]

        elif typ == "field":
            return [field for field in self if field.widget.name != "button"]

        return out



    def get_fields_by_tag(self, tag):
        out = []
        for field in self:
            if tag in field.tags:
                out.append(field)
        return out

    def set_visible(self, tag = None):
        """ Shows fields """
        if tag:
            items = self.get_fields_by_tag(tag)
        else:
            items = self

        for item in items:
            item.set_visible()

    def set_hidden(self, tag = None):
        """ Hides fields """
        if tag:
            items = self.get_fields_by_tag(tag)
        else:
            items = self

        for item in items:
            item.set_hidden()

    def set_disabled(self, tag = None):
        if tag:
            items = self.get_fields_by_tag(tag)
        else:
            item = self

        for item in items:
            item.set_disabled()

    def set_enabled(self, tag = None):
        if tag:
            items = self.get_fields_by_tag(tag)
        else:
            item = self

        for item in items:
            item.set_enabled()


    def handle_onClick(self, widget_name = None, **params):
        """ This event is not routed to the widget - it is handeled by the form itself. """
        self.target_widget = widget_name
        widget_obj = self[widget_name].widget
        cmd = widget_obj.params["on_click"] # widget must support "on_click"-param
        self.handle_event(cmd, event_params = params)

    def handle_onChange(self, widget_name = None, **params):
        """
        OnChange != ValueChange!
        OnChange is the additional event which can take place and normally will be fired directly.
        ValueChange is the event which the form-component needs to keep the server-side state up to date.
        It normally is enqueued and not fired directly.
        This event is not routed to the widget - it is handeled by the form itself.
        """
        self.target_widget = widget_name
        widget_obj = self[widget_name].widget
        cmd = widget_obj.params["on_change"] # widget must support "on_change"-param
        self.handle_event(cmd, event_params = params)

    def handle_ValueChange(self, widget_name = None, value = None):
        """ This one is called when a "this.notify_value_change()" is called from the widget-js.
        The data-type of "value" corresponds to the type the "get_value"-method of the
        js-part of the widget returns. You can transfer any complex data-type
        as long as the handle_ValueChange-Method of the widget can handle it correctly!
        Routing the event to the widget """
        self.target_widget = widget_name
        self[widget_name].widget.handle_ValueChange(value)

    def handle_GetData(self, widget_name = None, query = None):
        self.target_widget = widget_name
        self[widget_name].widget.handle_GetData(query)

    def handle_UploadFile(self, widget_name = None):
        self.target_widget = widget_name
        self[widget_name].widget.handle_UploadFile()








class PostData(dict):
    """
    The form wants the getlist method - no problem.
    """

    def __init__(self, page_request, data):
        self.page_request = page_request
        super(PostData, self).__init__(data)

    def getlist(self, key):
        v = self.page_request.getall(key)
        return list(v)


class FormDataProvider(object):
    """
    This handles the server-side-state-magic
    """

    def __init__(self, page_request, form_data_store, transaction):
        self.transaction = transaction
        self.in_params = page_request.params
        self.form_data_store = form_data_store


    def getlist(self, key):
        if self.transaction.is_created():
            return []
        elif self.in_params.has_key(key):
            return list(self.in_params.getall(key))
        elif key in self.form_data_store:
            return [self.form_data_store[key]]
        else:
            return []

    def __contains__(self, key):
        data = self.getlist(key)
        return True if data else False










# --------------- dynamic superclassing ---------------


class ChoicesWrapper(object):
    def __init__(self, field, choices):
        self.field = field
        self.choices = choices

    def __iter__(self):
        if type(self.choices) is str:
            if self.choices.startswith("self."):
                self.choices = self.choices[5:]
            if self.choices.endswith("()"):
                self.choices = self.choices[:-2]

            func = getattr(self.field.form_obj, self.choices)
            return self.l10n_iter(func())
        else:
            return self.l10n_iter(self.choices)

    def l10n_iter(self, choice):
        for key, label in choice:
            label = self.field.gettext(label)
            yield key, label


# --- wtforms extensions ---

SelectField__oinit__ = wtforms.fields.core.SelectField.__init__
def SelectField__init__(self, *args, **kwargs):
    SelectField__oinit__(self, *args, **kwargs)
    self.choices = ChoicesWrapper(self, self.choices)
wtforms.fields.core.SelectField.__init__ = SelectField__init__

def Field_tooltip(self):
    if self.description:
        return jinja2.Markup(u"<div class=\"epfl-form-tooltip\" title=\"{0}\"></div>".format(jinja2.escape(self.description)))
    else:
        return ""
wtforms.fields.core.Field.tooltip = Field_tooltip

