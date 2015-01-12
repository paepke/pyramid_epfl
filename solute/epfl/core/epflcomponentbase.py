# coding: utf-8

from pprint import pprint
from collections2 import OrderedDict as odict

import types, copy, string, inspect, uuid

from pyramid import security
from pyramid import threadlocal

from solute.epfl.core import epflclient, epflutil, epflexceptions
from solute.epfl.jinja import jinja_helpers

from solute.epfl import json

import jinja2
import jinja2.runtime
from jinja2.exceptions import TemplateNotFound


class UnboundComponent(object):
    """
    This is one of two main classes used by epfl users, though few will notice. Any ComponentBase derived subclass will
    return an UnboundComponent wrapping it, unless specifically instructed to return an instance. See
    ComponentBase.__new__ for further details.

    Warning: Instantiation should be handled by the epfl core!

    If you encounter an UnboundComponent you are likely trying to access a component in an untimely manner. Assign it a
    cid and access that component via page.cid after init_transaction() is done by ComponentContainerBase.
    ComponentContainerBase's add_component will return the actually instantiated component if it is called with an
    UnboundComponent.
    """

    __valid_subtypes__ = [bool, int, long, float, complex,
                          str, unicode, bytearray, xrange,
                          type, types.FunctionType,
                          types.NoneType]
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
        self.position = (self.__unbound_config__.get('cid', None) or uuid.uuid4().hex,
                         self.__unbound_config__.get('slot', None))

    def __call__(self, *args, **kwargs):
        """
        With this helper the UnboundComponent can be pseudo instantiated to return a new UnboundComponent from it's base
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
        """
        Pickling helper.
        """
        for param in self.__unbound_config__:
            self.assure_valid_subtype(self.__unbound_config__[param])
        return self.__unbound_cls__, self.__unbound_config__, self.position

    def __setstate__(self, state):
        """
        Pickling helper.
        """
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
        """
        Equality checking for an UnboundComponent means checking the class and config.
        """
        if type(other) is not UnboundComponent\
                or other.__unbound_cls__ != self.__unbound_cls__\
                or other.__unbound_config__ != self.__unbound_config__:
            return False

        return True


class ComponentBase(object):
    """ The base of all epfl-components
    Components are the building-blocks of any page (epflpage.Page) containing python, html, css and javascript.
    They can send ajax-events from its js-parts to the server-side py-parts. The py-parts can respond by
    sending back js-snipplets which will be executed in the browser.

    There are two kinds of html, css and javascript associated with any component: Static and dynamic.
    Static code will be loaded into the browser once per transaction (epfltransaction.Transaction), this is normally
    used for css and javascript. The css and javascript files are taken from the Components css_name and js_name
    respectively, both being lists of strings that are resolved via jinja2.
    Dynamic code will be loaded everytime a component is rendered to be inserted or reinserted into a new or existing
    transaction (epfltransaction.Transaction), this is normally used for html and javascript. The html and javascript
    files are taken from the Components string template_name and js_parts respectively, the latter being a list of
    strings that are resolved via jinja2.

    Components are instantiated every request, their state is managed by the page (epflpage.Page) and stored in the
    transaction (epfltransaction.Transaction). To facilitate this, every component must define which of its attributes
    is to be stored in the transaction (epfltransaction.Transaction) and which to be used as it is by default. To notify
    the page how to store and reinstantiate a Component there are two attributes: compo_state and compo_config

    compo_state is a list of strings naming attributes whose current and up to date value is stored into the
    transaction (epfltransaction.Transaction) at the end of a  request by the page (epflpage.Page) and loaded from the
    transaction (epfltransaction.Transaction) at the  beginning of a request.

    An example would be a forms input field whose value may change multiple times during a
    transaction (epfltransaction.Transaction), each request being changes uploaded via ajax.

    class InputField(ComponentBase):
        compo_state = ['value']


    compo_config: By default everything that is not in the compo_state will be the result of pythons instantiation process, all
    attributes being references to the attributes of the components class. For non trivial attributes this means that
    changes to class attributes will affect all instances of this class. compo_config offers an easy way to avoid this
    behaviour, by copying the attribute using copy.deepcopy from the class to the instance.

    """

    __acl__ = [(security.Allow, security.Everyone, 'access')] # a pyramid acl that defines the permissions for this component
                                                              # it only affects the has_access()-method.
                                                              # The base-component only defines the "access"-permission.
                                                              # If not given the component is not rendered.

    template_name = "empty.html" # filenames of the templates for this component (if any)
    js_parts = [] # filenames of the js-parts of this component
    js_name = [] # filenames of the js-files for this component (if any)
    css_name = [] # filenames of the css-files for this component (if any)
    compo_state = [] # which attributes of the object are persisted into the transaction
    compo_config = [] # all attributes declared here will be transformed into instance-variables
                      # (so it is safe to modify them during a request)

    visible = True # Is the component visible or not?

    # This should never be None, if it is and something breaks because of it the parameter has not been correctly passed
    # through the __new__/UnboundComponent pipe.
    __unbound_component__ = None
    struct_dict = None


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

        self = super(ComponentBase, cls).__new__(cls, **config)

        if self.__unbound_component__ is None:
            self.__unbound_component__ = cls()

        self.is_rendered = False # whas this componend rendered (so was the self.render-method called?
        self.redraw_requested = set() # all these parts of the component (or "main") want to be redrawn
        self.container_compo = None
        self.container_slot = None
        self.deleted = False

        self.template = None
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

        self.cid = args[1]
        self._set_page_obj(args[0])

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
        return {"class": self.__unbound_component__,
                "config": self.__config,
                "cid": self.cid,
                "slot": self.container_slot}

    @classmethod
    def create_by_compo_info(cls, page, compo_info, container_id):
        compo_obj = cls(page, compo_info['cid'], __instantiate__=True, **compo_info["config"])
        if container_id:
            container_compo = page.components[container_id] # container should exist before their content
            compo_obj.set_container_compo(container_compo, compo_info["slot"])
            container_compo.add_component_to_slot(compo_obj, compo_info["slot"])
        return compo_obj

    def _set_page_obj(self, page_obj):
        """ Will be called by __new__. Multiple initialisation-routines are called from here, so a component is only
        set up after being assigned its page.
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

        # now we can setup the component-state
        self.setup_component_state()

    def set_container_compo(self, compo_obj, slot, position=None):
        # TODO: Can be handled without traversal due to container_compo having a struct_dict reference.
        self.container_compo = compo_obj
        self.container_slot = slot

        # Traverse upwards in the structure to set the correct position for this component in transaction.
        def traverse(compo):
            container = getattr(compo, 'container_compo', None)
            structure_dict = self.page.transaction.setdefault("compo_struct", odict())
            if container:
                structure_dict = traverse(container)
            return structure_dict.setdefault(compo.cid, odict())

        if position is not None:
            self.struct_dict = traverse(self.container_compo).insert(self.cid, odict(), position)
        else:
            self.struct_dict = traverse(self.container_compo).setdefault(self.cid, odict())

    def delete_component(self):
        """ Deletes itself. You can call this method on dynamically created components. After it's deletion
        you can not use this component any longer in the layout. """
        if not self.container_compo:
            raise ValueError, "Only dynamically created components can be deleted"

        self.container_compo.del_component(self, self.container_slot)

        for attr_name in self.compo_state + self.base_compo_state:
            del self.page.transaction[self.cid + "$" + attr_name]
        del self.page.transaction[self.cid + "$__inited__"]
        self.add_js_response('epfl.destroy_component("{cid}");'.format(cid=self.cid))

        del self.page[self.cid]

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
        if not self.has_access():
            return False
        if check_parents:
            return not self.container_compo or self.container_compo.is_visible()

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
        ##todo: msg = epfli18n.get_text(msg)
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
            raise Exception('Received None as event handler, have you setup an '
                            'event handler for %s in %s?' % (event_name, self.__class__))
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

    def render_templates(self, env, templates):
        out = []
        if type(templates) is not list:
            templates = [templates]

        for template in templates:
            jinja_template = env.get_template(template)
            out.append(jinja_template.render(**self.get_render_environment(env)))
        return out

    def get_render_environment(self, env):
        return {'compo': self}

    def render(self, target='main'):
        """ Called to render the complete component.
        Used by a full-page render request.
        It returns HTML.
        """

        if not self.is_visible():
            # this is the container where the component can be placed if visible afterwards
            return jinja2.Markup("<div epflid='{cid}'></div>".format(cid = self.cid))

        self.is_rendered = True

        # Prepare the environment and output of the render process.
        env = self.request.get_epfl_jinja2_environment()

        out = ''
        if target == 'js':
            js_out = ''.join(self.render_templates(env, self.js_parts))
            if len(js_out) > 0:
                out += '<script type="text/javascript">%s</script>' % js_out
        elif target == 'js_raw':
            out += ''.join(self.render_templates(env, self.js_parts))
        elif target == 'main':
            out += ''.join(self.render_templates(env, self.template_name))

        return jinja2.Markup(out)

    def get_js_part(self, raw=False):
        """ gets the javascript-portion of the component """

        if not self.is_visible():
            # this js cleans up the browser for this component
            return self.js_call("epfl.destroy_component", self.cid)
        if raw:
            return self.render('js_raw')
        return self.render('js')

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
        if self.container_compo and "main" in self.container_compo.redraw_requested: # TODO: compo-parts!
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
            parts["main"] = self.render()

        if self.redraw_requested or self.is_rendered:
            parts["js"] = self.get_js_part(raw=True)

        return parts


    def __call__(self, *args, **kwargs):
        """ For direct invocation from the jinja-template. the args and kwargs are also provided by the template """
        return self.render(*args, **kwargs)

    def compo_destruct(self):
        """ Called before destruction of this component by a container component.

        [request-processing-flow]
        """
        pass


    def switch_component(self, target, cid, slot=None, position=None):
        """
        Switches a component from its current location (whatever component it may reside in at that time) and move it to
        slot and position in the component determined by the cid in target.
        After that assure_hierarchical_order is called to avoid components being initialized in the wrong order.
        """

        compo = getattr(self.page, cid)
        target = getattr(self.page, target)
        source = getattr(self.page, compo.container_compo.cid)

        struct_dict = source.struct_dict.pop(cid)
        source.components.remove(compo)

        compo.set_container_compo(target, slot)
        if position is None:
            target.struct_dict[cid] = struct_dict
            target.components.append(compo)
        else:
            target.struct_dict.insert(cid, struct_dict, position)
            target.components.insert(position, compo)

        target.redraw()
        source.redraw()


class ComponentContainerBase(ComponentBase):
    """
    This component automatically adds components based on the UnboundComponent objects its node_list contains once per
    transaction.

    Components inheriting from it can overwrite init_struct in order to dynamically return different lists per
    transaction instead of one static list for the lifetime of the epfl service.
    """
    template_name = 'tree_base.html'
    node_list = []
    compo_state = ['row_offset', 'row_limit', 'row_count']

    default_child_cls = None
    row_offset = 0
    row_limit = 30
    row_data = 30
    row_count = 30

    __update_children_done__ = False

    def __new__(cls, *args, **kwargs):
        self = super(ComponentContainerBase, cls).__new__(cls, *args, **kwargs)
        if isinstance(self, cls):
            self.setup_component_slots()

        return self

    def after_event_handling(self):
        super(ComponentContainerBase, self).after_event_handling()
        self.update_children(force=True)

    def update_children(self, force=False):
        """If a default_child_cls has been set this updates all child components to reflect the current state from
        get_data(). Will raise an exception if called twice without the force parameter present."""

        if self.__update_children_done__ and not force:
            raise Exception('update_children called twice without force parameter for component %s.' % self.cid)
        self.__update_children_done__ = True

        if self.default_child_cls is None:
            return
        data = self.get_data(self.row_offset, self.row_limit, self.row_data)
        # TODO: data may change without the actually displayed element changing!
        for i, d in enumerate(data):
            if i < len(self.components) and self.components[i].id == d['id']:
                continue
            if i < len(self.components):
                self.replace_component(self.components[i], self.default_child_cls(**d))
            else:
                self.add_component(self.default_child_cls(**d), position=i)
            self.redraw()

        for compo in self.components[len(data):]:
            compo.delete_component()
            self.redraw()

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        """ Overwrite this method to automatically provide data to this components children.

        The list must comprise of dict like data objects with an id key. The data objects will be used as parameters for
        the creation of a default_child_cls component."""
        return []

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        self.row_offset, self.row_limit, self.row_data = row_offset, row_limit, row_data

    def init_struct(self):
        return self.node_list

    def init_transaction(self):
        super(ComponentContainerBase, self).init_transaction()

        self.node_list = self.init_struct()

        for node in self.node_list:
            cid, slot = node.position

            self.add_component(node(self.page, cid, __instantiate__=True), slot=slot, cid=cid)
        self.update_children(force=True)

    def replace_component(self, old_compo_obj, new_compo_obj):
        """Replace a component with a new one. Handles deletion bot keeping position and cid the same."""
        cid = old_compo_obj.cid
        position = self.components.index(old_compo_obj)
        old_compo_obj.delete_component()
        return self.add_component(new_compo_obj(cid=cid), position=position)

    def add_component(self, compo_obj, slot = None, cid = None, position=None):
        """ You can call this function to add a component to its container.
        slot is an optional parameter to allow for more complex components, cid will be used if no cid is set to
        compo_obj, position can be used to insert at a specific location.
        """

        if isinstance(compo_obj, UnboundComponent):
            cid, slot = compo_obj.position
            compo_obj = compo_obj(self.page, cid, __instantiate__=True)

        # we have no nice cid, so use a UUID
        if not cid:
            cid = str(uuid.uuid4())
        # assign the container
        compo_obj.set_container_compo(self, slot, position=position)
        # handle the static part
        self.page.add_static_component(cid, compo_obj)
        # now remember it
        self.page.transaction["compo_info"][cid] = compo_obj.get_component_info()
        # and make it available in this container
        self.add_component_to_slot(compo_obj, slot, position=position)
        # the transaction-setup has to be redone because the component can
        # directly be displayed in this request.
        self.page.handle_transaction()

        return compo_obj

    def setup_component_slots(self):
        """ Overwrite me. This method must initialize the slots that this
        container-component provides to accumulate components """
        self.components = []

    def add_component_to_slot(self, compo_obj, slot, position=None):
        """ This method must fill the correct slot with the component """
        if position is not None:
            self.components.insert(position, compo_obj)
        else:
            self.components.append(compo_obj)

    def del_component(self, compo_obj, slot=None):
        """ Removes the component from the slot and form the compo_info """
        compo_obj.compo_destruct()
        if hasattr(compo_obj, 'components'):
            for compo in compo_obj.components[:]:
                compo.delete_component()
        self.components.remove(compo_obj)
        if self.struct_dict is None:
            self.page.transaction['compo_struct'][self.cid].pop(compo_obj.cid)
        else:
            self.struct_dict.pop(compo_obj.cid)
        self.page.transaction['compo_info'].pop(compo_obj.cid)
