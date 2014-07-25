# -*- coding: utf-8 -*-

import inspect
import string
import types
import copy
import datetime

import jinja2
from solute.epfl.jinja import jinja_helpers
from solute.epfl.core import epflclient, epflutil, epflexceptions

from wtforms.widgets.core import HTMLString


class WidgetBase(object):

    """ The base-class for all our widgets of the WTForms-System.
    These widgets are rendered by jinja-templates.

    The widgets are somehow higherlevel than normal WTForm-Widgets, they got some state in a
    shadow dict, which is managed by the component. And they are one-to-one instanciated to thier
    field. This state is modified by self.setup_state,
    and available though its field-object. The state is shared with its field.

    To create own widgets, inherit from this class and override the class-variables:

    name
    template_name
    js_name
    param_def

    """

    name = None # logischer Name des Widgets
    template_name = None # Als String: Dateiname des Templates (wird ab dem Hauptverzeichnis der Widgets gesucht)
                         # Als Dict: {"name": Dateiname des Templates,
                         #            "html": Name des Jinja-Macros für die HTML-Erzeugung
                         #            "js": Name des Jinja-Macros für die JS-Erzeugung}
    js_name = None # Dateiname der JS-Datei zum Widget (wird ab dem Hauptverzeichnis der Widgets gesucht)
    css_name = None # Filename of the CSS-File for this widget


    param_def = {} # Dict ala:
                   # "param_name": param_type
                   # z.B.
                   # param_def = {"min_value": int,
                   #              "max_value": int}

    @classmethod
    def split_field_kwargs(cls, kwargs):
        """ Gets a mixture of kwargs for the field and itself. This comes from the "unbound"-Field in
        form-class field definition. It looks into its param_def to decide if an option is for this widget
        or else for the field.
        """

        field_kwargs = {}
        widget_kwargs = {}

        for key, value in kwargs.items():
            if key in cls.param_def:
                widget_kwargs[key] = value
            else:
                field_kwargs[key] = value

        return field_kwargs, widget_kwargs


    @classmethod
    def add_pyramid_routes(cls, config):
        fn = inspect.getfile(cls)
        pos = fn.index("/epfl/widgets/")
        epos = fn.index("/", pos + 14)
        widget_path_part = fn[pos + 14 : epos]

        config.add_static_view(name = "epfl/widgets/" + widget_path_part,
                               path = "solute.epfl.widgets:" + widget_path_part + "/static")



    def __init__(self, **params):
        self.raw_params = params
        self.form = None
        self.state = None
        self.is_rendered = False # is this widget rendered
        self.js_part = None # after the rendering of the html-part this contains the js-part
        self.marked_error = False # sould this field be marked errorneous.

        self.params = {} # will be filled with persistable params and unpersistable params

    @property # some kind of late binding
    def page_request(self):
        return self.form.page_request

    @property # some kind of late binding
    def request(self):
        return self.form.request

    @property # some kind of late binding
    def response(self):
        return self.form.response

    def get_wid(self):
        wid = self.form.get_component_id() + "_" + self.field.name
        return wid

    def set_field(self, field):
        """ Called directly after the initialisation by epflfieldbase.FieldBase """
        self.field = field
        self.form = field.form
        # self.state will be initialized later...

    def init_state(self):
        """ Called once a transaction to fill in the default state of this widget.
        It's called throu the field.
        """

        self.state["widget_ready"] = True # so this function is only called once
        self.state["params"] = self.eval_params(persistable = True)


    def setup_state(self):
        """ Called just before the complete jina-template is rendered on all components registered in the page """

        self.state = self.form.get_field_state(self.field.name) # must be done here

        if "widget_ready" not in self.state:
            self.init_state()

        self.params = self.state["params"].copy()
        self.params.update(self.eval_params(persistable = False))

    def finalize_state(self):
        """ Called on page-finalisation (every roundtrip) """

        pass


    def get_render_macros(self):

        if type(self.template_name) is dict:
            template_name = self.template_name["template"]
            html_macro_name = self.template_name["html"]
            js_macro_name = self.template_name.get("js")
        else:
            template_name = self.template_name
            html_macro_name = "main"
            js_macro_name = "init_js"

        env = self.request.get_epfl_jinja2_environment()
        template = env.get_template(template_name)

        main_macro = getattr(template.module, html_macro_name)

        if js_macro_name:
            init_js_macro = getattr(template.module, js_macro_name)
        else:
            init_js_macro = None

        return main_macro, init_js_macro

    def pre_render(self):
        """ This is the place to modify internals of the field before rendering (the page).
        Overwrite me!
        """

        epflutil.add_extra_contents(self.response, obj = self)

        # # register the widget-js-tags
        # if self.js_name:
        #     js_script_src = epflclient.JSLink(self.get_js_script_src())
        #     self.response.add_extra_content(js_script_src)

        # # register the widget-css-tags
        # if self.css_name:
        #     css_script_src = epflclient.CSSLink(self.get_css_style_src())
        #     self.response.add_extra_content(css_script_src)

    def get_param_info(self, param_name):
        """ returns a dict with runtime-info about this widget-param """

        param_def = self.param_def[param_name]
        if type(param_def) is tuple:
            param_type, param_default = param_def
            raw_value = self.raw_params.get(param_name, param_default)
        else:
            param_type = param_def
            if param_name in self.raw_params:
                raw_value = self.raw_params[param_name]
            else:
                raw_value = None

        return {"raw_value": raw_value,
                "type": param_type}

    def eval_param(self, param_name):
        """ (Re)-Evaluates a widget-param.
        Mainly for Re-Evaluating purposes - e.g. refresh the domain of a select-box.
        """

        info = self.get_param_info(param_name)
        info_type = wrap_param_type(info["type"])
        value = info["type"].eval(info["raw_value"], self.form) # evaluate the param

        return value

    def eval_params(self, persistable):
        """ Evaluate the params passed to the widget at instanciation time
        """

        params = {}
        for param_name in self.param_def.keys():

            info = self.get_param_info(param_name)
            info_type = wrap_param_type(info["type"])

            if info_type.persist != persistable:
                continue

            if info_type.check_type(info["raw_value"]):
                value = info_type.eval(info["raw_value"], self.form) # evaluate the param
            else:
                raise epflexceptions.ConfigurationError, "Field '" + self.field.name + "' must define param '" + param_name + "' of type " + repr(info["type"]) + " got " + repr(info["raw_value"])

            params[param_name] = value

        return params

    def update_data_source(self, data_source):
        """ Will be called before rendering the widget.
        You can modify the data_source object (which is an instance of DataSource).
        """
        pass

    def __call__(self, field, **kwargs):

        if field is not self.field:
            raise RuntimeError, "This is not my field!"

        if not self.field.is_visible():
            return ""

        self.is_rendered = True

        client_side_params = {}
        for param_name in self.param_def.keys():
            info = self.get_param_info(param_name)
            info_type = wrap_param_type(info["type"])

            if info_type.client_param:
                client_side_params[param_name] = self.params[param_name]

        data_source = DataSource(form = self.form,
                                 widget = self,
                                 field = self.field,
                                 widget_kwargs = kwargs,
                                 widget_params = client_side_params)
        self.update_data_source(data_source)


        # render the widget-template:
        main_macro, init_js_macro = self.get_render_macros()

        # the "main"-html of this widget:
        html = main_macro(ds = data_source.get_data())

        # the init-js of this widget:
        # it is not returned here but saved
        self.js_part = init_js_macro(ds = data_source.get_data())

        return HTMLString(html)

    def get_js_part(self):
        return self.js_part

#    def get_js_script_src(self):
#        return [self.request.static_url(self.asset_spec + "/" + name) for name in self.js_name]

#    def get_css_style_src(self):
#        return [self.request.static_url(self.asset_spec + "/" + name) for name in self.css_name]

#    def get_param(self, param_name):
#        return self.state["params"][param_name]

    def make_html_attribute(self, attr_name, attr_value):
        """ returns a string to insert into a html-tag to define an html-attribue """
        return jinja2.Markup("{attr_name}=\"{attr_value}\"".format(attr_name = attr_name, attr_value = jinja2.escape(attr_value)))

    def js_call(self, method_name, *args):
        """ A JS-Snipped which calls a method of this widget """

        wid = self.form.get_component_id() + "_" + self.field.name

        if method_name.startswith("this."):
            js = ["epfl.components[\"" + self.form.cid + "\"].widgets[\"" + wid + "\"]" + method_name[4:]]
        else:
            js = [method_name]

        js.append("(")
        first = True
        for arg in args:
            if first:
                first = False
            else:
                js.append(",")
            js.append(json.encode(arg))
        js.append(")")

        return string.join(js, "")

    def has_errors(self):
        """ Checks if the field has errors """
        if self.field.errors or self.marked_error:
            return True
        else:
            return False

    def set_error(self, msg):
        """ Sets the error message for the field.
        A latter call of "validate" will clear/override this message. """
        self.field.errors.append(msg)

    def mark_error(self):
        """ Marks the field visually errornous. After a form.redraw the field appears red.
        The marker is not persisted in state. This means just like the self.errors
        it is only displayed once.
        """
        self.marked_error = True




class DataSource(object):

    """ The instance-variables are exposed to the template of the widget.
    e.g. access the

    name of the widget as {{ ds.name }}
    min_value of the SliderWidget (configured in the Form-Instance as param_def) as {{ ds.params.min_value }}
    some kwarg passed from the jinja-template while calling the widget by {{ ds.kwargs.some_name }}

    This object may be modified by the update_data_source-method of the concrete widget
    """

    def __init__(self, form, field, widget, widget_kwargs, widget_params):

        self.__dict__["data"] = {}

        self.form = form
        self.field = field
        self.widget = widget
        self.kwargs = widget_kwargs
        self.cid = form.get_component_id()
        self.name = field.name
        self.params = widget_params
        self.label = field.label
        self.wid = self.cid + "_" + self.name
        self.css_classes = jinja_helpers.StringJoinerList(" ")


        if widget.has_errors():
            self.css_classes.append("epfl-form-field-error-mark")

        self.value = self.field.visualize_func(field) # widget_kwargs.get("value", field.data)
        self.typed_value = field.data

    def get_data(self):
        return self.data

    def __setattr__(self, key, value):
        self.data[key] = value

    def __getattr__(self, key):
        return self.data[key]


class ParamType(object):

    persist = True        # will the param value be persisted into the server-side-state (not possible for unpickelable types)
    client_param = True   # will the param value be transfered to the client-side? (not possible for unjasonable-types)

    @classmethod
    def check_type(cls, obj):
        pass

    @classmethod
    def eval(cls, obj, form):
        return obj

class OptionalDomainType(ParamType):

    client_param = True

    @classmethod
    def check_type(cls, obj):
        typ = type(obj)
        if not obj:
            return True
        elif typ in types.StringTypes and obj.startswith("self."):
            return True # method-names starting with "self." are OK!
        else:
            return (typ is types.FunctionType) or (typ is list)

    @classmethod
    def eval(cls, obj, form):
        """ evaluates the value of the domain-widget-parameter (kwargs of the widget-instanciation in the form):
        - if the param is a function it will be called without arguments
        - if the param if a name of a method of the form (starts with "self.") the corresponding item will be returned
        - everything else will be directly used as the domain.
        """
        if type(obj) is types.FunctionType:
            return obj()
        elif type(obj) in types.StringTypes and obj.startswith("self."):
            domain_func_name = obj[5:] # cut of "self."
            domain_func_name = domain_func_name.rstrip("()") # strip "()"
            return getattr(form, domain_func_name)()
        else:
            return obj

class MethodType(ParamType):

    persist = False
    client_param = False

    @classmethod
    def check_type(cls, obj):
        typ = type(obj)
        if typ in types.StringTypes and obj.startswith("self."):
            return True # method-names starting with "self." are OK!
        else:
            return (typ is types.FunctionType)

    @classmethod
    def eval(cls, obj, form):
        """ evaluates the value of the widget-parameter (kwargs of the widget-instanciation in the form):
        - if the param is a function it will be returned
        - if the param if a name of a method of the form (starts with "self.") the corresponding item will be returned
        """
        if type(obj) is types.FunctionType:
            return obj
        elif type(obj) in types.StringTypes and obj.startswith("self."):
            domain_func_name = obj[5:] # cut of "self."
            domain_func_name = domain_func_name.rstrip("()")
            return getattr(form, domain_func_name)


class OptionalMethodType(MethodType):

    @classmethod
    def check_type(cls, obj):
        if obj is None:
            return True
        else:
            return super(cls, OptionalMethodType).check_type(obj)

class EventType(ParamType):
    """ An event: None - no event given, or a string - the name of the
    event-handler-method without the leading "handle_"
    e.g. "show_result" -> "handle_show_result" is the handler-function-name
    """

    @classmethod
    def check_type(cls, obj):
        return obj is None or type(obj) is str


class NumberType(ParamType):
    """ An integer or a float """

    @classmethod
    def check_type(cls, obj):
        return type(obj) in [int, float]

class OptionalNumberType(ParamType):

    @classmethod
    def check_type(cls, obj):
        if not obj:
            return True
        else:
            return type(obj) in [int, float]

class BooleanType(ParamType):
    @classmethod
    def check_type(cls, obj):
        return type(obj) is bool

class OptionalBooleanType(ParamType):

    @classmethod
    def check_type(cls, obj):
        if not obj:

            return True
        else:
            return type(obj) is bool


class DateType(ParamType):
    """ A simple date object of the datetime lib """

    @classmethod
    def check_type(cls, obj):
        return type(obj) is datetime.date

class OptionalDateType(ParamType):
    """ A simple date object of the datetime lib """

    @classmethod
    def check_type(cls, obj):
        if not obj:
            return True
        else:
            return type(obj) is datetime.date

class TimeType(ParamType):

    @classmethod
    def check_type(cls, obj):
        return type(obj) is datetime.time

class OptionalTimeType(ParamType):
    """ A simple time object of the datetime lib """

    @classmethod
    def check_type(cls, obj):
        if not obj:
            return True
        else:
            return type(obj) is datetime.time

class StringType(ParamType):

    @classmethod
    def check_type(cls, obj):
        return type(obj) in [str, unicode]

class OptionalStringType(ParamType):
    """ A String or nothing """

    @classmethod
    def check_type(cls, obj):
        if not obj:
            return True
        else:
            return type(obj) in [str, unicode]


class OptionalIntType(ParamType):
    """ An integer or nothing """

    @classmethod
    def check_type(cls, obj):
        if not obj:
            return True
        else:
            return type(obj) is int



def wrap_param_type(info_type):
    if inspect.isclass(info_type) and issubclass(info_type, ParamType):
        return info_type
    else:
        return ParamTypeWrapper(info_type)


class ParamTypeWrapper(ParamType):
    """ If a none-"ParamType"-Object is given as widget-param-type this class wraps it
    to something the epflwidgetbase can handle as "ParamType".
    """

    def __init__(self, param_type):
        self.param_type = param_type

    def eval(self, raw_value, form_obj):
        return copy.deepcopy(raw_value)

    def check_type(self, raw_value):
        return type(raw_value) is self.param_type
