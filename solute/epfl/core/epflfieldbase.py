# -*- coding: utf-8 -*-

import types
from wtforms.widgets.core import HTMLString
import wtforms
from wtforms import validators
import traceback

def get_response():
    """ Getting the response from the thread-local-service """
    return __svc__.epfl.ctx.response

# the coerce funcs have two tasks:
# 1. convert a value coming from the client (eventually a string) to the corresponding python-value
# 2. raise an error if this is not possible
# they are the flipside of the "visualize"-funcs
def coerce_func_char(data, max_length = None):
    if data is None:
        data = ""
    if max_length and len(unicode(data)) > max_length:
        raise ValueError, "String is to long"
    return unicode(data)

def coerce_func_int(data):
    if data is None:
        return None
    elif not unicode(data).strip():
        return None
    else:
        return int(data)

def coerce_func_long(data):
    if data is None:
        return None
    elif not unicode(data).strip():
        return None
    else:
        return long(data)

def coerce_func_float(data):
    if data is None:
        return None
    elif not unicode(data).strip():
        return None
    else:
        return float(data)

def coerce_func_bool(data):
    if data is None:
        return None
    elif not unicode(data).strip():
        return None
    elif data == "True" or data == True:
        return True
    else:
        return False

# the visualize-funcs have the taks to convert the python-server-side-value
# to an apropriate client-side representation
def visualize_func_standard(field):
    data = field.data
    if data is None:
        data = ""

    return data


def bing():
    try:
        raise Exception
    except Exception as err:
        traceback.print_stack()


class FieldBase(wtforms.Field):

    """ The base-class for all our fields of the WTForms-System.

    The semantics of fields and widgets differs from the original-WTForms-idea.
    Since the more complex part of forms are widgets, not fields, this FieldBase augments
    the widgets. Widget instances are now directly bound to thier field instances which are bound
    to the form instance. The main difference is that you can now access your field from the widget in
    every method. That's better!

    """

    is_template_element = True # Needed for template-reflection: this makes me a template-element (like a component)
    default_field_type = "char"
    default_field_value = None # can be overridden by kwargs of the field, here it can be also a function, that evaluates
                               # to the default value

    def __init__(self, *field_args, **kwargs):

        self.coerce_func = None # the function to coerce a value from the client to the server-type
                                # due to the wtforms-design the func must also accept server-type values and
                                # return them unmodified
        self.visualize_func = None # the function to convert a value from server to client-representation
        self.max_length = None
        self._data = None

        self.field_type = kwargs.pop("type", self.default_field_type)  # types: "char", "char(X)", "int", "float"
        self.default_validators = kwargs.pop("validators", [])
        self.default_mandatory = kwargs.pop("mandatory", False)
        self.default_visible = kwargs.pop("visible", True)
        self.default_enabled = kwargs.pop("enabled", True)
        self.default_writeable = kwargs.pop("writeable", True)

        tags = kwargs.pop("tags", [])
        if type(tags) is list:
            self.tags = set(tags)
        else:
            self.tags = set(tags.split())

        field_kwargs, widget_kwargs = self.widget_class.split_field_kwargs(kwargs) # which params are for the field, which for the widget?
        self.form = kwargs["_form"]
        self.widget = self.widget_class(**widget_kwargs) # Widget-Class -> Widget
        self.widget.set_field(self)

        super(FieldBase, self).__init__(*field_args, **field_kwargs)

        if "default" not in field_kwargs:
            if type(self.default_field_value) is types.FunctionType:
                self.default = self.default_field_value()
            else:
                self.default = self.default_field_value

        self.setup_type()

        if self.name == "submit":
            raise ValueError, "'submit' is really a bad name for a field!"

#    """ The following methods are for adding more control over the self.data-value of a field.
#    self.pre_setting_data and self.pre_getting_data are hooks you can overwrite in subclasses """
#    @property
#    def data(self):
#        self.pre_getting_data()
#        return self._data
#    @data.setter
#    def data(self, value):
#        self.pre_setting_data(value)
#        self._data = value
#    def pre_getting_data(self):
#        pass
#    def pre_setting_data(self, value):
#        pass
    

    @property # some kind of late binding...
    def page_request(self):
        return self.form.page_request

    def init_state(self):
        """ Called once a transaction """

        self.state["field_ready"] = True
        self.state["mandatory"] = self.default_mandatory
        self.state["visible"] = self.default_visible
        self.state["writeable"] = self.default_writeable
        self.state["enabled"] = self.default_enabled


    def setup_state(self):
        """ Called from the form just before the rendering """
        self.state = self.form.get_field_state(self.name)

        if "field_ready" not in self.state:
            self.init_state()

        self.setup_validators()

    def finalize_state(self):
        pass


    def setup_type(self):
        """ handles the different data-types for this field.
        It manages the coerceion-function. """

        if self.field_type == "char":
            self.coerce_func = coerce_func_char
            self.visualize_func = visualize_func_standard
            self.coerce_error_msg = "txt_value_must_be_unicode"
        elif self.field_type.startswith("char("):
            self.max_length = int(self.field_type[5:-1])
            self.visualize_func = visualize_func_standard
            self.coerce_func = lambda s, max_length = self.max_length: coerce_func_char(s, max_length)
            self.coerce_error_msg = "txt_value_too_long"
        elif self.field_type == "int":
            self.coerce_func = coerce_func_long
            self.visualize_func = visualize_func_standard
            self.coerce_error_msg = "txt_value_must_be_integer"
        elif self.field_type == "float":
            self.coerce_func = coerce_func_float
            self.visualize_func = visualize_func_standard
            self.coerce_error_msg = "txt_value_must_be_float"
        elif self.field_type == "bool":
            self.coerce_func = coerce_func_bool
            self.visualize_func = visualize_func_standard
            self.coerce_error_msg = "txt_value_must_be_boolean"
        else:
            raise TypeError, "Field-Type " + repr(self.__class__.__name__) + " does not support type: " + repr(self.field_type)

    def setup_validators(self):

        self.validators = self.default_validators[:]
        self.validator_visual = ""

##        if self.field_type == "int":
##            self.validators.append(FieldMandatory())
##        elif self.field_type == "float":
##            self.validators.append(FieldMandatory())

        if self.state["mandatory"]:
            self.validators.append(FieldMandatory())

        for v in self.validators:
            visual = getattr(v, 'visual', None)
            if visual:
                self.validator_visual = visual


    def process_formdata(self, valuelist):
        """ This one is called with the data comming from the transaction-state (server-side-data) or from the query-params (client-side-data).
        When comming from the transaction-state the value may be the old one (the one before the ValueChange-Event was handeled).
        So self.process_errors must be cleared, if the type was coerced sucessfully.

        Also calling this is the handle_ValueChange (with the value as one-element-list). In this case the type of the value is already
        correct (JSON is typed) but the "format" still is the client-side representation. E.g. the type is "string" client and server. but
        the server has ISO-date-formatted timestamp and the client human-readable-formatted timestamp.

        Due to the wtforms-design the coerce-func must also accept server-type values and
        return them unmodified

        """
        if valuelist:
            try:
                self.data = self.coerce_func(valuelist[0])
                self.process_errors = []
            except (ValueError, TypeError) as e:
                self.data = valuelist[0]
                if self.is_visible() and self.coerce_func:
                    self.process_errors.append(self.coerce_error_msg)

    def process_data(self, data):
        """ called with the default value """
        super(FieldBase, self).process_data(data)

    def after_form_set_data(self):
        """ A convenience hook, that is called after a form.set_data() was executed.
        Here the framework will update the state of the field that depends on self.data.
        E.g. a suggest-field will update its entry-data.
        You must do the same, if a field uses this hook if you manipulate self.data by your self.
        """
        pass


    def create_new_value(self):
        """ Called if form.validate was called with create_new_values=True for every field.
        Here a field (e.g. Suggest) can check, if a new value must be created by the application-model
        that the field can be validated correctly.
        """
        pass


##    def pre_validate(self, form):
##        """ This uses the self.coerce_func set up by setup_type. It's called when self.validate() is called. """

##        if not self.is_visible():
##            return
##        elif self.data is None:
##            return
##        elif not unicode(self.data).strip():
##            return

##        if not self.coerce_func:
##            return

##        try:
##            dummy = self.coerce_func(self.data) # just call the coerceion to see if it fails
##        except (ValueError, TypeError) as e:
##            raise ValueError(self.gettext(self.coerce_error_msg))


    def post_validate(self, form, stopped):
        """ Called after all validators. Used to clean up the error-messages in case of hidden fields """

        if not self.is_visible():
            self.errors = []

    def reset_data(self):
        """ Resets the value of the field to the default """
        self.data = self.default

    def is_visible(self):
        """ Calculates the visibility. This depends on the configuration (self.set_visible() / self.set_hidden() )
        and the access-control-system. """
        return self.state["visible"]


    def set_visible(self):
        """ The field is now visible """
        self.state["visible"] = True

    def set_hidden(self):
        """ The field is now invisible """
        self.state["visible"] = False

    def set_enabled(self):
        """ The field is now enabled. """
        self.state["enabled"] = True

    def set_disabled(self):
        """ The field is now disabled.
        This means, the field is relevant for the user and can be filled out (when it's also writeable) """
        self.state["enabled"] = False

    def set_writeable(self):
        """ The field can now be edited. """
        self.state["writeable"] = True

    def set_readonly(self):
        """ The field now only displays it's value but is not editable """
        self.state["writeable"] = False

    def set_mandatory(self):
        """ The Field is now mandatory """
        self.state["mandatory"] = True

    def set_optional(self):
        """ The Field is now optional """
        self.state["mandatory"] = False

    def set_error(self, msg):
        """ Sets the error message for the field. 
        A latter call of "validate" will clear/override this message. """
        self.errors.append(msg)

    def mark_error(self):
        """ Marks the field visually errornous. After a form.redraw the field appears red. 
        The marker is not persisted in state. This means just like the self.errors
        it is only displayed once.
        """
        self.widget.mark_error()


class FieldMandatory(object):
    """
    Validates that the field contains data. This validator will stop the
    validation chain on error.

    If the data is empty, also removes prior errors (such as processing errors)
    from the field.

    Mandatory means:
    "" => error
    0 => OK
    "0" => OK
    None => error

    """
    field_flags = ('required', )
    visual = "*"

    def __init__(self, message = "txt_value_required"):
        self.message = message

    def __call__(self, form, field):

        if field.data is None:
            error = True
        elif not unicode(field.data).strip():
            error = True
        else:
            error = False

        message = field.gettext(self.message)

        if error:
            field.errors[:] = []
            raise validators.StopValidation(message)

