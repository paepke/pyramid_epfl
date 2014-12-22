# coding: utf-8

from pprint import pprint

import types, copy, string, inspect, uuid

from pyramid import security
from pyramid import threadlocal

from solute.epfl.core import epflclient, epflutil, epflexceptions
from solute.epfl.jinja import jinja_helpers

from solute.epfl import json

import jinja2
import jinja2.runtime
from jinja2.exceptions import TemplateNotFound


class CallableWrapper(object):
    cls, name = None, ''
    _function = None

    def __init__(self, *args):
        self.__setstate__(args)

    def __getstate__(self):
        return self.cls, self.name

    def __setstate__(self, state):
        self.cls, self.name = state

    def __call__(self, *args, **kwargs):
        if not self._function:
            self._function = getattr(self.cls, self.name)
        return self._function(*args, **kwargs)


class UnboundComponent(object):
    """
    This is one of two main classes used by epfl users. Any ComponentBase derived subclass will yield an
    UnboundComponent wrapping it, unless specifically instructed to yield a real instance. See ComponentBase.__new__ for
    further details.

    Instantiation should normally be handled by the epfl core!

    If you encounter an UnboundComponent you are likely trying to access a component in an untimely manner. Assign it a
    cid and access that component via page.cid after init_transaction() is done by ComponentTreeBase.

    Both ComponentTreeBase and ComponentContainerBase's add_component will return the actually instantiated component if
    they are called with an UnboundComponent.
    """

    __valid_subtypes__ = [bool, int, long, float, complex,
                          str, unicode, bytearray, xrange,
                          type, types.FunctionType, CallableWrapper]
    __debugging_on__ = False
    __dynamic_class_store__ = None

    def __init__(self, cls, config):
        """
        Unbound components handle:
        1. Dynamic class creation with inheritance from cls and attributes on the new class as defined in config.
        2. Dynamic cid generation for unbound components without a cid entry in config.
        3. Sanity checks for all attributes if epfl.debug mode is enabled.
        """
        self.__unbound_cls__ = cls
        self.__unbound_config__ = config.copy()

        # Copy config and create a cid if none exists.
        self.position = (self.__unbound_config__.get('cid', uuid.uuid4().hex),
                         self.__unbound_config__.get('slot', None))

    def __call__(self, *args, **kwargs):
        """
        With this helper the UnboundComponent can be pseudo instantiated to yield a new UnboundComponent from it's base
        class. Additionally this can be used to generate an instance if one is needed if the __instantiate__ keyword is
        set to True.
        """
        if kwargs.pop('__instantiate__', None) is None:
            config = self.__unbound_config__.copy()
            config.update(kwargs)
            return UnboundComponent(self.__unbound_cls__, config)
        else:
            self.__unbound_config__.update(kwargs)
            self.__dynamic_class_store__ = None
            kwargs['__instantiate__'] = True

        cls = self.__dynamic_class__
        return cls(*args, **kwargs)

    @property
    def __dynamic_class__(self):
        """
        If the config contains entries besides cid and slot a dynamic class is generated.
        This feature offers just in time creation of the actual class object to be used by epfl.
        """
        if self.__dynamic_class_store__:
            return self.__dynamic_class_store__

        stripped_conf = self.__unbound_config__.copy()
        stripped_conf.pop('cid', None)
        stripped_conf.pop('slot', None)
        if len(stripped_conf) > 0:
            self.__dynamic_class_store__ = type(self.__unbound_cls__.__name__ + '_auto_' + uuid.uuid4().hex,
                                                (self.__unbound_cls__, ),
                                                {})
            for param in self.__unbound_config__:
                self.assure_valid_subtype(self.__unbound_config__[param])
                setattr(self.__dynamic_class_store__, param, self.__unbound_config__[param])
            setattr(self.__dynamic_class_store__, '__unbound_component__', self)
            return self.__dynamic_class_store__
        else:
            return self.__unbound_cls__

    def create_by_compo_info(self, *args, **kwargs):
        """
        Expose the ComponentBase class method in order to allow storing UnboundComponent instances instead of raw
        classes. This is required in order to have dynamic classes at all with a pickling session store, since only
        static classes can be pickled.

        The class needs to be setup with all dynamic attributes
        """
        return self.__dynamic_class__.create_by_compo_info(*args, **kwargs)

    def __getstate__(self):
        for param in self.__unbound_config__:
            self.assure_valid_subtype(self.__unbound_config__[param])
        return self.__unbound_cls__, self.__unbound_config__, self.position

    def __setstate__(self, state):
        self.__unbound_cls__, self.__unbound_config__, self.position = state

    @staticmethod
    def assure_valid_subtype(param):
        """
        Raise an exception if param is not among the valid subtypes or contains invalid subtypes.
        ***epfl.debug***: This test is skipped if epfl.debug is set to False in the config.
        """

        # Safely read the epfl.debug flag from the settings.
        registry = threadlocal.get_current_registry()
        if not registry or not registry.settings or not registry.settings.get('epfl.debug', 'false') == 'true':
            return

        # There are some basic types that are always accepted.
        if type(param) in UnboundComponent.__valid_subtypes__:
            return

        # If param is in the list of iterables all its entries are checked.
        if type(param) in [list, tuple, set, frozenset]:
            for item in param.__iter__():
                UnboundComponent.assure_valid_subtype(item)
            return
        # If param is a dict all its entries are checked.
        if type(param) is dict:
            for item in param.values():
                UnboundComponent.assure_valid_subtype(item)
            return

        if type(param) in [UnboundComponent]:
            return
        raise Exception('Tried adding unsupported %r to an unbound class.' % param)

    def __eq__(self, other):
        if type(other) is not UnboundComponent\
                or other.__unbound_cls__ != self.__unbound_cls__\
                or other.__unbound_config__ != self.__unbound_config__:
            return False

        return True


class ComponentBase(object):

    """ The base of all epfl-components
    Components are logical building-blocks of a page (epflpage.Page). It consists of html, python, css and js-parts.
    Components can send ajax-events from its js-parts to the server-side py-parts. The py-parts can respond by
    sending back js-snipplets which will be executed in the browser.

    this is a lie!!!
##    The Jinja-Template is exposed throu its "main"-macro - a jinja-macro which is called "main" defined in the component-template.
##    All other jinja-macros are exposed throu self.macros.*, so the page-layout can use parts of the component or rearrange them as needed by the
##    html-layout.
    explain component-layout inheritance and inline-components and component-parts

    Since all component-instances only survive one request, you can not use "normal" object-attributes to save the state of your component.
    The state may be the index of the first row that is currently displayed to the user of a table, or the currenlty selected row.
    To solve this problem you can declare object-attributes as part of the "component-state". Just list the names of the attributes in the
    "compo_state"-class-variable.

    compo_state = ["start_row", "selcted_rows"]

    Now you can use self.start_row just as a normal object-attribute. But the framework stores and restores its value into the page-transaction. These
    attributes are also exposed as GET/POST-Parameters (prefixed with the component-id).

    Since a component is a class and since component-config are class variables they are shared between all requests. This is maybe not what you want!
    To define a class variable as a component-config-variable (this means the class-variable will be transformed in an instance-variable) put it's name
    into the compo_config - list.

    compo_state vs. compo_config: all attributes named in compo_state are persisted in the transaction, the compo_config's are not!

    """

    __acl__ = [(security.Allow, security.Everyone, 'access')] # a pyramid acl that defines the permissions for this component
                                                              # it only affects the has_access()-method.
                                                              # The base-component only defines the "access"-permission.
                                                              # If not given the component is not rendered.

    template_name = "empty.html" # filename of the template for this component (if any)
    js_name = [] # filenames of the js-files for this component (if any)
    css_name = [] # filenames of the css-files for this component (if any)
    compo_state = [] # which attributes of the object are persisted into the transaction
    compo_config = [] # all attributes declared here will be transformed into instance-variables
                      # (so it is safe to modify them during a request)

    visible = True # Is the component visible or not?

    # This should never be None, if it is and something breaks because of it the parameter has not been correctly passed
    # through the __new__/UnboundComponent pipe.
    __unbound_component__ = None


    base_compo_state = ["visible"] # these are the compo_state-names for this ComponentBase-Class

    is_template_element = True # Needed for template-reflection: this makes me a template-element (like a form-field)

    def __new__(cls, *args, **config):
        """
        epfl wraps component creation at this stage to allow custom __init__ functions without interfering with
        component creation by the system.

        Calling a class derived from ComponentBase will normally yield an UnboundComponent unless __instantiate__=True
        has been passed as a keyword argument.

        Any component developer may thus overwrite the __init__ method without causing any problems in order to expose
        runtime settable attributes for code completion and documentation purposes.
        """
        if config.pop('__instantiate__', None) is None:
            return UnboundComponent(cls, config)

        if not getattr(cls, '__unbound_component__'):
            setattr(cls, '__unbound_component__', cls())

        self = super(ComponentBase, cls).__new__(cls, **config)

        self.is_rendered = False # whas this componend rendered (so was the self.render-method called?
        self.redraw_requested = set() # all these parts of the component (or "main") want to be redrawn
        self.container_compo = None
        self.container_slot = None
        self.deleted = False

        self.template = None
        self.parts = None
        self.macros = None
        self.__config = config

        for attr_name in self.compo_config:
            if attr_name in config:
                config_value = config[attr_name]
            else:
                config_value = getattr(self, attr_name)

            setattr(self, attr_name, copy.deepcopy(config_value)) # copy from class to instance

        for attr_name in self.compo_state + self.base_compo_state:
            if attr_name in config:
                config_value = config[attr_name]
                setattr(self, attr_name, copy.deepcopy(config_value))

        return self

    def __init__(self, *args, **kwargs):
        """
        Overwrite-me for auto completion features on component level.
        """
        pass

    @classmethod
    def add_pyramid_routes(cls, config):
        """ Adds the routes needed by this component """
        fn = inspect.getfile(cls)
        pos = fn.index("/epfl/components/")
        epos = fn.index("/", pos + 17)
        compo_path_part = fn[pos + 17 : epos]

        config.add_static_view(name = "epfl/components/" + compo_path_part,
                               path = "solute.epfl.components:" + compo_path_part + "/static")


    def get_component_info(self):
        if self.container_compo:
            container_id = self.container_compo.cid
        else:
            container_id = None
        return {"class": self.__unbound_component__,
                "config": self.__config,
                "cid": self.cid,
                "slot": self.container_slot,
                "cntrid": container_id}

    @classmethod
    def create_by_compo_info(cls, page, compo_info):
        compo_obj = cls(__instantiate__=True, **compo_info["config"])
        if compo_info["cntrid"]:
            container_compo = page.components[compo_info["cntrid"]] # container should exist before thier content
            compo_obj.set_container_compo(container_compo, compo_info["slot"])
            container_compo.add_component_to_slot(compo_obj, compo_info["slot"])
        return compo_obj


    def set_component_id(self, id):
        """ Tells the component its component-id. The component-id is the name of the attribute of the page object to which
        the component was assined.
        This function is called by the __setattr__-function of the page-object
        """
        self.cid = id

    def set_page_obj(self, page_obj):
        """ Will be called by epflpage.Page by the __setattr__-trick.
        Multiple initialisation-routines are called from here, so a component is only
        correctly setup AFTER is was assined to its page.
        """
        self.page = page_obj
        self.page_request = page_obj.page_request
        self.request = page_obj.request
        self.response = page_obj.response

        # setup template

        if not self.template_name:
            raise epflexceptions.ConfigurationError, "You did not setup the 'self.template_name' in " + repr(self)


        env = self.request.get_epfl_jinja2_environment()
        self.template = env.get_template(self.template_name)
        self.macros = jinja_helpers.MacroAccessor(self.template)
        self.parts = ComponentPartAccessor(self) # this one does all the inline-compo/compo-part-inheritance magic!

        # now we can setup the component-state
        self.setup_component_state()

    def set_container_compo(self, compo_obj, slot):
        self.container_compo = compo_obj
        self.container_slot = slot

    def delete_component(self):
        """ Deletes itself. You can call this method on dynamically created components. After it's deletion
        you can not use this component any longer in the layout. """
        if not self.container_compo:
            raise ValueError, "Only dynamically created components can be deleted"

        self.container_compo.del_component(self, self.container_slot)
        self.deleted = True

    def finalize(self):
        """ Called from the page-object when the page is finalized
        [request-processing-flow]
        """
        self.finalize_component_state()

    def has_access(self):
        """ Checks if the current user has sufficient rights to see/access this component.
        Normally called by a condition in the jinja-template.
        """

        if security.has_permission("access", self, self.request):
            return True
        else:
            return False

    def set_visible(self):
        """ Shows the complete component. You need to redraw it!
        It returns the visibility it had before.
        """
        current_visibility = self.visible
        self.visible = True
        return current_visibility

    def set_hidden(self):
        """ Hides the complete component. You need to redraw it!
        It returns the visibility it had before.
        """
        current_visibility = self.visible
        self.visible = False
        return current_visibility

    def is_visible(self, check_parents = False):
        """ Checks wether the component should be displayed or not. This is affected by "has_access" and
        the "visible"-component-attribute.
        If check_parents is True, it also checks if the template-element-parents are all visible - so it checks
        if this compo is "really" visible to the user.
        """
        if not self.visible:
            return False
        elif check_parents:
            if self.has_access():
                for compo_obj in self.get_template_parentelements():
                    if not compo_obj.is_visible():
                        return False
                return True
            else:
                return False
        else:
            return self.has_access()


    def add_ajax_response(self, resp_string):
        """ Adds to the response some string (ajax or js or whatever the clients expects here).
        Not to be confused with self.add_js_link (which adds a js-file to the page at full-page-request-time).
        In conjunction with callback-functions to a epfl.send(event, cb_func) call consider using "return_ajax_response".
        The Callback-Function then gets the ajax-response as first argument. Do not forget to json.encode(...) the data.
        Use only if sure that this was an ajax-request. If not so sure, use "add_js_response".
        """
        self.response.add_ajax_response(resp_string)

    def return_ajax_response(self, resp_string):
        """ Nearly the same as "add_ajax_response". Only difference: Only this response is returned, nothing else.
        This is needed if you make the request with epfl.send() and use a callback to process the returned data.
        Only with this function you can be sure, that nothing else from other components is sent back.
        """
        self.response.answer_json_request(resp_string)

    def add_js_response(self, js_string):
        """ Shortcut to epflpage """
        self.page.add_js_response(js_string)

    def init_transaction(self):
        """
        This function will be called only once a transaction for this component.
        It is called just before the event-handling of the page take place,
        so the state of all components is already completely setup (self.setup_component_state).

        You can overwrite this method to manipulate the initial state once.
        Use this to load data-objects you want to manipulate within this transaction.

        Nothing is done here, so the component does not need to call the super-function!

        [request-processing-flow]
        """
        pass


    def setup_component_state(self):
        """
        This function sets up the compo_state attributes.
        It is called every request. It copies the attribute-values from the transaction to the object.
        Warning: Only the state of this component is set up. You can not rely on any other component here!
        Overwrite this one if you need some additional setup of the component state.

        [request-processing-flow]
        """

        for attr_name in self.compo_state + self.base_compo_state:
            value = self._get_compo_state_attribute(attr_name)
            setattr(self, attr_name, value)

    def setup_component(self):
        """ Called from the system every request when the component-state of all
        components in the page is setup.
        Here component-individual additional setup can be made.
        This is called after a potential call to "init_transaction".
        So no events have been handled so far.

        [request-processing-flow]
        """
        pass

    def after_event_handling(self):
        """ Called from the system every request after all events
        for all components have been handeled.
        Here component-individual additional modifications can be made.

        [request-processing-flow]
        """
        pass



    def _get_compo_state_attribute(self, attr_name):
        transaction = self.page.transaction
        if self.cid + "$" + attr_name in transaction:
            value = transaction[self.cid + "$" + attr_name]
            return value
        else:
            return copy.deepcopy(getattr(self, attr_name))


    def show_fading_message(self, msg, typ = "ok"):
        """ Shortcut to epflpage.show_fading_message(msg, typ).
        typ = "info" | "ok" | "error"
        """
        return self.page.show_fading_message(msg, typ)

    def show_message(self, msg, typ = "info"):
        """ Shortcut to epflpage.show_message(msg, typ)
        typ = "info" | "ok" | "error"
        """
        return self.page.show_message(msg, typ)

    def show_confirm(self, msg, cmd_ok):
        """
        Displays a box with "ok" and "cancel" to the user.
        If the user clicks "ok" the event named in "cmd_ok" will be fired.
        """
##todo        msg = epfli18n.get_text(msg)
        js = """if (confirm(%s)) {
                    var ev = epfl.make_component_event("%s", "%s", {});
                    epfl.send(ev);
             }""" % (json.encode(msg), self.cid, cmd_ok)

        self.page.add_js_response(js)


    def finalize_component_state(self):
        """
        This function finalizes the compo_state attributes
        """

        values = {}

        for attr_name in self.compo_state + self.base_compo_state:
            value = getattr(self, attr_name)
            values[self.cid + "$" + attr_name] = value

        if self.deleted:
            for attr_name in values:
                del self.page.transaction[attr_name]
        else:
            self.page.transaction.update(values)


    def get_component_id(self):
        return self.cid

    def js_call(self, method_name, *args):
        """ returns a js-snipped calling a method of this component (if method_name starts with
        'this.'), and the given parameters.
        The parameters are escaped and quoted as necessary """

        if method_name.startswith("this."):
            js = ["epfl.components[\"" + self.cid + "\"]" + method_name[4:]]
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

    def handle_event(self, event_name, event_params):
        """
        Called by the system for every ajax-event in the ajax-event-queue from the browser.
        epflpage.Page.handle_ajax_request routes the event to the corresponding component -
        identified by it´s "component_id" (self.cid).
        May be overridden by concrete components.
        """

        event_handler = getattr(self, "handle_" + event_name, None)
        if event_handler is None:
            raise Exception('Received None as event handler, have you setup an event handler?')
        elif not hasattr(event_handler, '__call__'):
            raise Exception('Received non callable for event handling.')
        event_handler(**event_params)

    def request_handle_submit(self, params):
        """
        Called by the system (epflpage.Page.handle_submit_request) with the CGI-params once for
        every non-ajax-request
        Overwrite me!
        """
        pass


    def pre_render(self):
        """ Called just before the page jina-rendering occures.
        Overwrite me!!!
        """

        epflutil.add_extra_contents(self.response, obj = self)



    def render(self, *args, **kwargs):
        """ Called to render the complete component.
        Used by a full-page render request.
        It returns HTML.
        """

        if not self.is_visible():
            # this is the container where the component can be placed if visible afterwards
            return jinja2.Markup("<div epflid='{cid}'></div>".format(cid = self.cid))

        self.is_rendered = True

        # the "main"-html of this component:
        for_redraw = kwargs.pop("for_redraw", False)
        if for_redraw:
            main_macro = self.parts.redraw_main
        else:
            main_macro = self.parts.main
        return main_macro(*args, **kwargs)

    def get_js_part(self):
        """ gets the javascript-portion of the component """

        if not self.is_visible():
            # this js cleans up the browser for this component
            return self.js_call("epfl.destroy_component", self.cid)

        init_js_macro = self.parts.js
        return init_js_macro()

    def notify_render_inline(self):
        """ This one is called from the modified template (by the epfl-component-jinja-extension).
        It's injected into the body of a inline-component-macro. So it is called when this component is
        rendered. (Or a part - excluding js - of it)
        """
        self.is_rendered = True

    def redraw(self, parts = None):
        """ This requests a redraw. All components that are requested to be redrawn are redrawn when
        the ajax-response is generated (namely page.handle_ajax_request()).
        You can specify the parts that need to be redrawn (as string, as list or None for the complete component).
        If a super-element (speaking of template-elements) of this component wants to be redrawn -
        this one will not reqeust it's redrawing.
        """
        for compo_obj in self.get_template_parentelements():
            if "main" in compo_obj.redraw_requested: # TODO: compo-parts!
                return # a parent of me already needs redrawing!

        if type(parts) is list:
            self.redraw_requested.update(set(parts))
        elif parts is None:
            self.redraw_requested.add("main")
        else:
            self.redraw_requested.add(parts)

    def get_redraw_parts(self):
        """ This is used to redraw the component. In contrast to "render" it returns a dict with the component-parts
        as keys and thier content as values. No modification of the "response" is made. Only the parts that are
        requested to be redrawn are returned in the dict. The "js" part is special. It is rendered if some other 
        part of the component is requested (means actively by the programmer) or rendered (means passively by
        e.g. rerendering the container-component).
        """

        self.pre_render()
        parts = {}

        if "main" in self.redraw_requested:
            parts["main"] = self.render(for_redraw = True)
        else:
            for part_name in self.redraw_requested:
                parts[part_name] = self.parts[part_name]()

        if self.redraw_requested or self.is_rendered:
            parts["js"] = self.get_js_part()

        return parts


    def __call__(self, *args, **kwargs):
        """ For direct invocation from the jinja-template. the args and kwargs are also provided by the template """
        return self.render(*args, **kwargs)

    def get_template_subelements(self):
        """ Returns all subelements of this component rendered by the template.
        Subelements are other components or widgets. Only container-like components have subelements.
        This is done by using the template-reflection.
        """

        out = []

        ri = self.page.get_template_reflection_info()
        compo_ri = ri.get_element_by_name(self.page, self.cid)

        if not compo_ri:
            return out

        for el in compo_ri.get_subelements():
            compo_accessor, part_accessor = el.get_accessors()
            compo_obj = self.page.components.get(compo_accessor)
            if compo_obj:
                template_element = compo_obj._get_template_element(part_accessor)
                if template_element and template_element not in out:
                    out.append(template_element)

        return out

    def get_template_parentelements(self):
        """ Returns all the template-elements of this component up to the root-template-element.
        Parent-Elements only can be container-like components.
        This is done by using the template-reflection.
        """

        out = []

        ri = self.page.get_template_reflection_info()
        compo_ri = ri.get_element_by_name(self.page, self.cid)

        if not compo_ri:
            return []

        parent_ri = compo_ri
        while True:
            parent_ri = parent_ri.get_parent()
            if not parent_ri:
                break

            compo_accessor, part_accessor = parent_ri.get_accessors()
            compo_obj = self.page.components.get(compo_accessor)
            if compo_obj:
                out.append(compo_obj)

        return out

    def _get_template_element(self, part_accessor):
        """ A method used by "get_template_subelements". Here the component must implement the logic to access
        its subelements (e.g. the form has widgets)
        """
        return self

    def overwrite_compopart(self, name, part):
        """ Is called from the template by "{% %}"
        """
        setattr(self.template.module, "compopart_" + name, part)

    def switch_component(self, target, cid, slot=None, position=None):
        """
        Switches a component from its current location (whatever component it may reside in at that time) and move it to
        slot and position in the component determined by the cid in target.
        After that assure_hierarchical_order is called to avoid components being initialized in the wrong order.
        """

        compo = getattr(self.page, cid)
        target = getattr(self.page, target)
        source = getattr(self.page, compo.container_compo.cid)

        self.page.transaction["compo_info"].remove(compo.get_component_info())

        position_index = -1
        counter = -1
        for key, value in enumerate(self.page.transaction["compo_info"]):
            if value.get('cid', None) == self.cid and position is not None:
                counter += 1
            if value.get('cntrid', None) == self.cid and position is not None:
                counter += 1
            if counter > position:
                position_index = key
                break

        source.components.remove(compo)
        compo.set_container_compo(target, slot)
        if position is None:
            position = -1
        target.components.insert(position, compo)

        self.page.transaction["compo_info"].insert(position_index, compo.get_component_info())
        self.assure_hierarchical_order()

        target.redraw()
        source.redraw()

    def assure_hierarchical_order(self):
        """
        Recursively applies the correct order on all compo_info dicts in the transaction. This has to be used after
        changing component order to ensure that all container components are initialized before their respective content
        components.
        """
        def order_recursive(input, seen_key=set()):
            if len(input) == 0:
                return []
            new_seen_key = set()
            output = []
            withheld = []
            for v in input:
                if v['cntrid'] is None or v['cntrid'] in seen_key:
                    output.append(v)
                    new_seen_key.add(v['cid'])
                else:
                    withheld.append(v)
            seen_key.update(new_seen_key)

            output += order_recursive(withheld, seen_key)
            return output
        self.page.transaction["compo_info"] = order_recursive(self.page.transaction["compo_info"])


class ComponentPartAccessor(object):
    """ Used to access the component-part-macros inside a template. If the macro is not defined, a nice error will be raised.
    Access the macros in dict-style.
    It implements the fall-thou-logic from inline-definition to component-definition of parts
    """

    def __init__(self, compo_obj):
        self.compo_obj = compo_obj
        self.compo_template = compo_obj.template
        self.debug = compo_obj.request.registry.settings["epfl.debug"]

    def __getitem__(self, key):
        return getattr(self, key)

    def parseAttributeError(self, excep):
        """ Parse the message of an AttributeError-Exception.
        """
        tokens = excep.message.split()
        return {"missing_attribute": tokens[-1].strip("'")}

    def snip_script_tags(self, data):
        data = data.strip()
        if data.startswith("<script"):
            data = data[data.index(">") + 1:]
        if data.endswith("</script>"):
            data = data[:-9]
        return data


    def get_macro(self, template_obj, macro_name):
        if self.debug:
            try:
                return getattr(template_obj.module, macro_name)
            except AttributeError, e:
                info = self.parseAttributeError(e)
                raise AttributeError, "Template '{0}' has no component-part named '{1}'. Please define {{% compopartdef {1} () %}}!".format(template_obj.filename, info["missing_attribute"][10:])
        else:
            return getattr(template_obj.module, macro_name)

    def get_redraw_template(self):
        template_name = self.compo_obj.page.template + " redraw:" + self.compo_obj.cid
        if self.compo_obj.request.is_template_marked_as_not_found(template_name):
            return None

        try:
            env = self.compo_obj.request.get_epfl_jinja2_environment()
            template = env.get_template(template_name)
        except TemplateNotFound:
            self.compo_obj.request.mark_template_as_not_found(template_name)
            return None
        else:
            return template


    def __getattr__(self, key):
        """ Access the macro as dict-style-attribute """

        macro = None
        redraw_template = None

        if self.compo_template:
            # now looking throu the component-template (if there is one)

            if key == "main":
                # the "main" macro is named "main" and defined in the component-template
                macro = self.get_macro(self.compo_template, "main")
            elif key == "redraw_main":
                # the macro for redrawing a component may be defined in the page-template named "redraw_CID"...
                redraw_template = self.get_redraw_template() # a lot of magic!
                if not redraw_template:
                    # ... or it's simply the main-macro of the compo-template
                    macro = self.get_macro(self.compo_template, "main")
            else:
                # everything else is a part of the compo defined in the compo-template
                macro = self.get_macro(self.compo_template, "compopart_" + key)

        if macro:

            def macro_wrapper(*args, **kwargs):
                """ this one does the rendering (zwiebeld because of the 'self' parameter of the macro).
                The rendering of a single part of a component marks the component as "rendered".
                This implies the rendering of the js-part of this component. """

                if "caller" in kwargs:
                    has_caller = True
                else:
                    has_caller = False

                self.compo_obj.is_rendered = True # please render my js-part!
                if key == "js":
                    js = macro(self.compo_obj, has_caller, *args, **kwargs)
                    return self.snip_script_tags(js) + ";"
                else:
#                    import pdb; pdb.set_trace()
                    return macro(self.compo_obj, has_caller, *args, **kwargs)

            return macro_wrapper

        elif redraw_template:

            def template_wrapper(*args, **kwargs):
                """ this one does the rendering (zwiebeld because this is not a macro but a template).
                The rendering of a single part of a component marks the component as "rendered".
                This implies the rendering of the js-part of this component. """

                self.compo_obj.is_rendered = True # please render my js-part!

                ctx = self.compo_obj.page.get_template_ctx()

                return redraw_template.render(**ctx)

            return template_wrapper

        else:

            raise AttributeError, key


class ComponentContainerBase(ComponentBase):

    def __new__(cls, *args, **kwargs):
        self = super(ComponentContainerBase, cls).__new__(cls, *args, **kwargs)
        if isinstance(self, cls):
            self.setup_component_slots()
        return self

    def add_component(self, compo_obj, slot = None, cid = None):
        """ You can call this function to add a component to its container. Optional is the slot-name. 
        """

        if isinstance(compo_obj, UnboundComponent):
            cid, slot = compo_obj.position
            compo_obj = compo_obj(__instantiate__=True)

        # we have no nice cid, so use a UUID
        if not cid:
            cid = str(uuid.uuid4())
        # assign the container
        compo_obj.set_container_compo(self, slot)
        # handle the static part
        self.page.add_static_component(cid, compo_obj)
        # now remember it
        self.page.transaction["compo_info"].append(compo_obj.get_component_info())
        # and make it available in this container
        self.add_component_to_slot(compo_obj, slot)
        # the transaction-setup has to be redone because the component can
        # directly be displayed in this request.
        self.page.handle_transaction()

        return compo_obj

    def setup_component_slots(self):
        """ Overwrite me. This method must initialize the slots that this
        container-component provides to accumulate components """
        self.components = []

    def add_component_to_slot(self, compo_obj, slot):
        """ This method must fill the correct slot with the component """
        self.components.append(compo_obj)

    def del_component(self, compo_obj, slot):
        """ Removes the component from the slot and form the compo_info """
        self.components.remove(compo_obj)

        # remove it from the compo_info
        self.page.transaction["compo_info"] = [ci for ci in self.page.transaction["compo_info"]
                                               if ci["cid"] != compo_obj.cid]


class ComponentTreeBase(ComponentContainerBase):
    """
    This component automatically adds components based on the UnboundComponent objects its node_list contains once per
    transaction.

    Components inheriting from it can overwrite init_tree_struct in order to dynamically return different lists per
    transaction instead of one static list for the lifetime of the epfl service.
    """
    template_name = 'tree_base.html'
    node_list = []

    def init_tree_struct(self):
        return self.node_list

    def init_transaction(self):
        super(ComponentTreeBase, self).init_transaction()

        self.node_list = self.init_tree_struct()

        for node in self.node_list:
            cid, slot = node.position

            self.add_component(node(__instantiate__=True), slot=slot, cid=cid)