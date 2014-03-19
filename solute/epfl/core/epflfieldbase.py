# -*- coding: utf-8 -*-

import types
from wtforms.widgets.core import HTMLString
import wtforms
from wtforms import validators
import traceback

def get_response():
    """ Getting the response from the thread-local-service """
    return __svc__.epfl.ctx.response


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


    def __init__(self, *field_args, **kwargs):

        self.coerce_func = None
        self.max_length = None

        self.field_type = kwargs.pop("type", "char")  # types: "char", "char(X)", "int", "float"
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

        self.setup_type()

        if self.name == "submit":
            raise ValueError, "'submit' is really a bad name for a field!"

    @property
    def request(self):
        return self.form.request

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
            self.coerce_error_msg = "txt_value_must_be_unicode"
        elif self.field_type.startswith("char("):
            self.max_length = int(self.field_type[5:-1])
            self.coerce_func = lambda s, max_length = self.max_length: coerce_func_char(s, max_length)
            self.coerce_error_msg = "txt_value_too_long"
        elif self.field_type == "int":
            self.coerce_func = coerce_func_long
            self.coerce_error_msg = "txt_value_must_be_integer"
        elif self.field_type == "float":
            self.coerce_func = coerce_func_float
            self.coerce_error_msg = "txt_value_must_be_float"
        else:
            raise TypeError, "Unknown field type: " + repr(self.field_type)

    def setup_validators(self):

        self.validators = self.default_validators[:]
        self.validator_visual = ""

        if self.state["mandatory"]:
            self.validators.append(FieldMandatory(message = "txt_value_required"))

        for v in self.validators:
            visual = getattr(v, 'visual', None)
            if visual:
                self.validator_visual = visual


    def process_formdata(self, valuelist):
        """ This one is called with the data comming from the transaction-state or from the query-params.
        When comming from the transaction-state the value may be the old one (the one before the ValueChange-Event was handeled).
        So additionally the self.pre_validate is adapted to fire the validation-errors when calling self.validate() (now with the updated values)

        Also calling this is the handle_ValueChange (with the value as one-element-list). In this case the type of the value is already
        correct (JSON is typed) but small adjustments in the representation may be done (e.g. floats get the decimal-point).
        """
        if valuelist:
            try:
                self.data = self.coerce_func(valuelist[0])
            except (ValueError, TypeError) as e:
                self.data = valuelist[0]

    def process_data(self, data):
        """ called with the default value """
        super(FieldBase, self).process_data(data)


    def pre_validate(self, form):
        """ This uses the self.coerce_func setup by setup_type. It's called when self.validate() is called. """

        if not self.is_visible():
            return
        elif self.data is None:
            return
        elif not unicode(self.data).strip():
            return

        try:
            dummy = self.coerce_func(self.data) # just call the coerceion to see if it fails
        except (ValueError, TypeError) as e:
            raise ValueError(self.gettext(self.coerce_error_msg))


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

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):

        if field.data is None:
            error = True
        elif not unicode(field.data).strip():
            error = True
        else:
            error = False


        if error:
            if self.message is None:
                self.message = field.gettext('This field is required.')

            field.errors[:] = []
            raise validators.StopValidation(self.message)

