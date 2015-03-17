# coding: utf-8

from pprint import pprint
from collections2 import OrderedDict as odict
from collections import MutableSequence

import types, copy, string, inspect, uuid

from pyramid import security
from pyramid import threadlocal

from solute.epfl.core import epflclient, epflutil, epflacl

import ujson as json

import jinja2
import jinja2.runtime
from jinja2.exceptions import TemplateNotFound


class MissingContainerComponentException(Exception):
    pass


class MissingEventHandlerException(Exception):
    pass


class UnboundComponent(object):
    """
    This is one of two main classes used by epfl users, though probably few will notice. Any
    :class:`.ComponentBase` derived subclass will return an :class:`.UnboundComponent` wrapping it, unless specifically
    instructed to return an instance. See :func:`ComponentBase.__new__` for further details.

    Warning: Instantiation should be handled by the epfl core!

    If you encounter an :class:`.UnboundComponent` you are likely trying to access a component in an untimely manner.
    Assign it a cid and access that component via page.cid after init_transaction() is done by
    :class:`.ComponentContainerBase`. :func:`ComponentContainerBase.add_component` will return the actually
    instantiated component if it is called with an :class:`.UnboundComponent`.
    """

    __valid_subtypes__ = [bool, int, long, float, complex, str, unicode, bytearray, xrange, type, types.FunctionType,
                          types.NoneType]
    __debugging_on__ = False

    __dynamic_class_store__ = None  #: Internal caching for :attr:`UnboundComponent.__dynamic_class__`

    def __init__(self, cls, config):
        """
        Create dynamic cid for unbound components without a cid entry in config, store the calling class and create a
        copy of the config.
        """
        self.__unbound_cls__ = cls
        self.__unbound_config__ = config.copy()

        # Copy config and create a cid if none exists.
        self.position = (self.__unbound_config__.pop('cid', None) or uuid.uuid4().hex,
                         self.__unbound_config__.pop('slot', None))

    def __call__(self, *args, **kwargs):
        """
        Pseudo instantiation helper that returns a new UnboundComponent by updating the config. This can also be used to
        generate an instantiated Component if one is needed with the __instantiate__ keyword set to True.
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

    @classmethod
    def create_from_state(cls, state):
        ubc = cls(None, {})
        ubc.__setstate__(state)
        return ubc

    @property
    def __dynamic_class__(self):
        """
        If the config contains entries besides cid and slot a dynamic class is returned. This offers just in time
        creation of the actual class object to be used by epfl.
        """
        if self.__dynamic_class_store__:
            return self.__dynamic_class_store__

        stripped_conf = self.__unbound_config__.copy()
        stripped_conf.pop('cid', None)
        stripped_conf.pop('slot', None)
        if len(stripped_conf) > 0:
            self.__dynamic_class_store__ = type('%s_auto_%s' % (self.__unbound_cls__.__name__, uuid.uuid4().hex),
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
        Expose the :func:`ComponentBase.create_by_compo_info` in order to allow storing UnboundComponent instances
        instead of raw classes. This is required in order to have dynamic classes at all with a pickling session store,
        since only static classes can be pickled. The class is setup with all dynamic attributes by
        :func:`__dynamic_class__`.
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
        Checks class and config equality.
        """
        if type(other) is not UnboundComponent \
                or other.__unbound_cls__ != self.__unbound_cls__ \
                or other.__unbound_config__ != self.__unbound_config__:
            return False

        return True

    def __repr__(self):
        return '<UnboundComponent of {cls} with config {conf}>'.format(cls=self.__unbound_cls__,
                                                                       conf=self.__unbound_config__)


@epflacl.epfl_acl(['access'])
class ComponentBase(object):
    """
    Components are the building-blocks of any :class:`.epflpage.Page` containing python, html, css and javascript.
    Ajax-events are sent by javascript to the server-side python-parts. They can respond by sending back javascript
    which will be executed in the browser.

    There are two kinds of html, css and javascript associated with any component: Static and dynamic.
    Static code will be loaded into the browser once per :class:`.epfltransaction.Transaction`, this is normally
    used for css and javascript. The css and javascript files are taken from the Components css_name and js_name
    respectively, both being lists of strings that are resolved via jinja2.
    Dynamic code will be loaded everytime a component is rendered to be inserted or reinserted into a new or existing
    :class:`.epfltransaction.Transaction`, this is normally used for html and javascript. The html and javascript
    files are taken from the Components string template_name and js_parts respectively, the latter being a list of
    strings that are resolved via jinja2.

    Components are instantiated every request, their state is managed by the :class:`.epflpage.Page` and stored in the
    :class:`.epfltransaction.Transaction`. To facilitate this, every component must define which of its attributes
    is to be stored in the :class:`.epfltransaction.Transaction` and which to be used as it is by default. To notify
    the :class:`.epflpage.Page` how to store and reinstantiate a Component there are two attributes: compo_state and
    compo_config

    compo_state is a list of strings naming attributes whose current and up to date value is stored into the
    :class:`.epfltransaction.Transaction` at the end of a  request by the :class:`.epflpage.Page` and loaded from the
    :class:`.epfltransaction.Transaction` at the  beginning of a request.

    As an example see the following forms input field whose value may change multiple times during an
    :class:`.epfltransaction.Transaction`, requests for example being changes uploaded via ajax.

    .. code:: python

        class InputField(ComponentBase):
            compo_state = ['value']


    compo_config: By default everything that is not in the compo_state will be the result of pythons instantiation
    process, all attributes being references to the attributes of the components class. For non trivial attributes this
    means that changes to class attributes will affect all instances of this class. compo_config offers an easy way to
    avoid this behaviour, by copying the attribute using copy.deepcopy from the class to the instance.

    """

    template_name = "empty.html"  #: Filename of the template for this component (if any).
    js_parts = []  #: List of files to be parsed as js-parts of this component.
    js_name = []  #: List of javascript files to be statically loaded with this component.
    css_name = []  #: List of css files to be statically loaded with this component.
    compo_state = []  #: List of object attributes to be persisted into the :class:`.epfltransaction.Transaction`.
    compo_config = []  #: List of attributes to be copied into instance-variables using :func:`copy.deepcopy`.

    #: Flag this component as event sink, any event will stop here if True. If no handler is found it is discarded.
    event_sink = False

    visible = True  #: Flag for component rendering. Use via :func:`set_visible` and :func:`set_hidden`.

    #: Internal reference to this Components :class:`UnboundComponent`. If it is None and something breaks because of it
    #: this component has not been correctly passed through the :func:`__new__`/:class:`UnboundComponent` pipe.
    __unbound_component__ = None

    epfl_event_trace = None  #: Contains a list of CIDs an event bubbled through. Only available in handle\_ methods

    base_compo_state = ["visible"]  # these are the compo_state-names for this ComponentBase-Class

    is_template_element = True  # Needed for template-reflection: this makes me a template-element (like a form-field)

    is_rendered = False  #: True if this component was rendered calling :meth:`render`
    redraw_requested = None  #: Set of parts requesting to be redrawn.

    _compo_info = None
    _access = None

    @classmethod
    def add_pyramid_routes(cls, config):
        """ Adds the static pyramid routes needed by this component. This only works for native components stored in
        :mod:`solute.epfl.components`. """
        fn = inspect.getfile(cls)
        pos = fn.index("/epfl/components/")
        epos = fn.index("/", pos + 17)
        compo_path_part = fn[pos + 17: epos]

        config.add_static_view(name="epfl/components/" + compo_path_part,
                               path="solute.epfl.components:" + compo_path_part + "/static")

    @classmethod
    def create_by_compo_info(cls, page, compo_info, container_id):
        compo_obj = cls(page, compo_info['cid'], __instantiate__=True, **compo_info["config"])
        if container_id:
            container_compo = page.components[container_id]  # container should exist before their content
            compo_obj.set_container_compo(container_compo, compo_info["slot"])
            container_compo.add_component_to_slot(compo_obj, compo_info["slot"])
        return compo_obj

    def __new__(cls, *args, **config):
        """
        Calling a class derived from ComponentBase will normally return an UnboundComponent via this method unless
        __instantiate__=True has been passed as a keyword argument.

        Any component developer may thus overwrite the :func:`__init__` method without causing any problems in order to
        expose runtime settable attributes for code completion and documentation purposes.
        """
        if config.pop('__instantiate__', None) is None:
            return UnboundComponent(cls, config)

        self = super(ComponentBase, cls).__new__(cls, **config)

        if self.__unbound_component__ is None:
            self.__unbound_component__ = cls()

        self.redraw_requested = set()
        self.deleted = False

        self.__config = config

        for attr_name in self.compo_config:
            if attr_name in config:
                config_value = config[attr_name]
            else:
                config_value = getattr(self, attr_name)

            setattr(self, attr_name, copy.deepcopy(config_value))  # copy from class to instance

        self.cid = args[1]
        self._set_page_obj(args[0])

        return self

    def __init__(self, *args, **kwargs):
        """
        Overwrite this for auto completion features on component level.
        """
        pass

    def __getattribute__(self, key):
        if key not in ['compo_state', 'base_compo_state', 'cid', 'is_visible', '_themes', '_access'] \
                and key in self.compo_state + self.base_compo_state:
            return self.compo_info.get('compo_state', {}).get(key,
                                                              super(ComponentBase, self).__getattribute__(key))
        return super(ComponentBase, self).__getattribute__(key)

    def __setattr__(self, key, value):
        if key not in self.compo_state + self.base_compo_state:
            return super(ComponentBase, self).__setattr__(key, value)
        self.compo_info.setdefault('compo_state', {})[key] = value

    @property
    def compo_info(self):
        if self._compo_info is None:
            self._compo_info = self.page.transaction.get_component(self.cid)
        return self._compo_info or {}


    @property
    def struct_dict(self):
        return self.compo_info.setdefault('compo_struct', odict())

    @property
    def container_slot(self):
        return self.compo_info.get('slot', None)

    @container_slot.setter
    def container_slot(self, value):
        self.compo_info['slot'] = value

    @property
    def container_compo(self):
        if self.compo_info.get('ccid', None) is None\
                or 'ccid' not in self.compo_info\
                or self.compo_info['ccid'] is None:
            return None
        return getattr(self.page, self.compo_info['ccid'])

    @container_compo.setter
    def container_compo(self, value):
        self.compo_info['ccid'] = value.cid

    @profile
    def register_in_transaction(self, container, slot=None, position=None):
        compo_info = {'class': self.__unbound_component__.__getstate__(),
                      'ccid': container.cid,
                      'cid': self.cid,
                      'slot': slot}
        self.page.transaction.set_component(self.cid, compo_info, position=position, compo_obj=self)

    def get_component_info(self):
        info = {"class": self.__unbound_component__.__getstate__(),
                "config": self.__config,
                "cid": self.cid,
                "slot": self.container_slot}
        if getattr(self, 'container_compo', None) is not None:
            info['ccid'] = self.container_compo.cid
        return info

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
            raise Exception("You did not setup the 'self.template_name' in " + repr(self))

        # now we can setup the component-state
        self.setup_component_state()

    def set_container_compo(self, compo_obj, slot, position=None):
        """
        Set the container_compo for this component and create any required structural information in the transaction.
        """

        self.container_compo = compo_obj
        self.container_slot = slot

    def delete_component(self):
        """ Deletes itself. You can call this method on dynamically created components. After it's deletion
        you can not use this component any longer in the layout. """
        if not self.container_compo:
            raise ValueError("Only dynamically created components can be deleted")

        self.container_compo.del_component(self, self.container_slot)

        self.page.transaction.del_component(self.cid)
        self.add_js_response('epfl.destroy_component("{cid}");'.format(cid=self.cid))

        self.page.transaction['__initialized_components__'].remove(self.cid)

    def finalize(self):
        """ Called from the page-object when the page is finalized
        [request-processing-flow]
        """
        pass

    def has_access(self):
        """ Checks if the current user has sufficient rights to see/access this component.
        Normally called by a condition in the jinja-template.
        """
        if self._access is None:
            self._access = security.has_permission("access", self, self.request)
        return self._access

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

    @profile
    def is_visible(self, check_parents=False):
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
        compo_info = transaction.get_component(self.cid)

        return (compo_info or {}).get('compo_state', {}).get(attr_name, copy.deepcopy(getattr(self, attr_name)))

    def show_fading_message(self, msg, typ="ok"):
        """ Shortcut to epflpage.show_fading_message(msg, typ).
        typ = "info" | "ok" | "error"
        """
        return self.page.show_fading_message(msg, typ)

    def show_message(self, msg, typ="info"):
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

    @epflacl.epfl_has_permission('access')
    def handle_event(self, event_name, event_params):
        """
        Called by the system for every ajax-event in the ajax-event-queue from the browser.
        epflpage.Page.handle_ajax_request routes the event to the corresponding component -
        identified by it´s "component_id" (self.cid).
        May be overridden by concrete components.
        """

        event_handler = getattr(self, "handle_" + event_name, None)
        epfl_event_trace = event_params.pop('epfl_event_trace', [])
        try:
            if event_handler is None:
                raise MissingEventHandlerException('Received None as event handler, have you setup an '
                                                   'event handler for %s in %s? %s' % (event_name,
                                                                                       self.__class__,
                                                                                       epfl_event_trace))
            elif not hasattr(event_handler, '__call__'):
                raise MissingEventHandlerException('Received non callable for event handling.')

            # Special handling for drag_stop event in order to provide a stable position argument.
            if event_name in ['drag_stop', 'drop_accepts']:
                if len(epfl_event_trace) > 0:
                    last_compo = getattr(self.page, epfl_event_trace[-1])
                    compo = getattr(self.page, event_params['cid'])
                    position = self.components.index(last_compo)
                    if compo in self.components and self.components.index(compo) < position:
                        position -= 1
                    event_params.setdefault('position', position)

            self.epfl_event_trace = epfl_event_trace
            event_handler(**event_params)
            self.epfl_event_trace = None
        except MissingEventHandlerException:
            if self.event_sink is True:
                pass
            elif self.container_compo is not None:
                event_params.setdefault('epfl_event_trace', epfl_event_trace).append(self.cid)
                self.container_compo.handle_event(event_name, event_params)
            elif event_name in ['drag_stop', 'drop_accepts']:
                pass
            else:
                raise

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

        epflutil.add_extra_contents(self.response, obj=self)

    @profile
    def render_templates(self, env, templates):
        """
        Render one or many templates given as list using the given jinja2 environment env and the dict from
        :meth:`get_render_environment` as kwargs.
        """
        out = []
        if type(templates) is not list:
            templates = [templates]

        for template in templates:
            jinja_template = env.get_template(template)
            out.append(jinja_template.render(**self.get_render_environment(env)))
        return out

    def get_render_environment(self, env):
        """
        Creates a dictionary containing a reference to the component that is used as render kwargs.
        """
        return {'compo': self}

    @profile
    def render(self, target='main'):
        """ Called to render the complete component.
        Used by a full-page render request.
        It returns HTML.
        """

        if not self.is_visible():
            # this is the container where the component can be placed if visible afterwards
            return jinja2.Markup("<div epflid='{cid}'></div>".format(cid=self.cid))

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
            set_component_info = 'epfl.set_component_info("%(cid)s", "handle", %(handles)s);'
            set_component_info %= {'cid': self.cid,
                                   'handles': self.get_handles()}
            handles = self.get_handles()
            if handles:
                # Add with execution_order set to 1 so it will be done after the defaults.
                self.add_js_response((1, set_component_info))

        return jinja2.Markup(out)

    def get_handles(self):
        return [name[7:] for name in dir(self) if name.startswith('handle_') and name != 'handle_event']

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

    def redraw(self, parts=None):
        """ This requests a redraw. All components that are requested to be redrawn are redrawn when
        the ajax-response is generated (namely page.handle_ajax_request()).
        You can specify the parts that need to be redrawn (as string, as list or None for the complete component).
        If a super-element (speaking of template-elements) of this component wants to be redrawn -
        this one will not reqeust it's redrawing.
        """
        # if self.container_compo and "main" in self.container_compo.redraw_requested:  # TODO: compo-parts!
        #     return  # a parent of me already needs redrawing!

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

        self.page.transaction.switch_component(cid, target)


class ComponentContainerBase(ComponentBase):
    """
    This component automatically adds components based on the UnboundComponent objects its node_list contains once per
    transaction.

    Components inheriting from it can overwrite init_struct in order to dynamically return different lists per
    transaction instead of one static list for the lifetime of the epfl service.
    """
    template_name = 'tree_base.html'
    theme_path_default = 'container/default_theme'
    #: List of folders to check for additional theme parts. May inherit from or extend previous themes by using < for
    #: extending ({{ caller() }} will be the previous template) or > for inheriting (result of the last template will be
    #: placed as {{ caller() }} inside the previous template).
    theme_path = []

    #: Used to generate the children of this component.
    node_list = []

    compo_config = ['node_list']
    compo_state = ['row_offset', 'row_limit', 'row_count', 'row_data']

    default_child_cls = None
    data_interface = {'id': None}

    row_offset = 0
    row_limit = 30
    row_data = {}
    row_count = 30

    #: Updates are triggered every request in after_event_handling if True.
    auto_update_children = True
    #: Update is triggered initially in :meth:`init_transaction` if True
    auto_initialize_children = True

    __update_children_done__ = False

    components_initialized = False

    _themes = {}

    def __new__(cls, *args, **kwargs):
        self = super(ComponentContainerBase, cls).__new__(cls, *args, **kwargs)
        if isinstance(self, cls):
            self.setup_component_slots()

        return self

    @profile
    def get_themed_template(self, env, target):
        """
        Return a list of templates in the order they should be used for rendering. Deals with template inheritance based
        on the theme_path and the target templates found in the folders of the theme_path.
        """
        theme_paths = self.theme_path
        if type(theme_paths) is dict:
            theme_paths = theme_paths.get(target, theme_paths['default'])
        render_funcs = []
        direction = '<'
        for theme_path in reversed(theme_paths):
            try:
                if theme_path[0] in ['<', '>']:
                    direction = theme_path[0]
                    render_funcs.insert(0, env.get_template('%s/%s.html' % (theme_path[1:], target)).module.render)
                    continue
                tpl = env.get_template('%s/%s.html' % (theme_path, target))
                render_funcs.append(tpl.module.render)
                return direction, render_funcs
            except TemplateNotFound:
                continue

        tpl = env.get_template('%s/%s.html' % (self.theme_path_default, target))
        render_funcs.append(tpl.module.render)

        return direction, render_funcs

    @profile
    def get_render_environment(self, env):
        """
        Creates a dictionary containing references to the different theme parts and the component. Theme parts are
        wrapped as callables containing their respective inheritance chains as defined by :attr:`theme_path`.
        """
        result = {}

        def wrap(cb, parent=None):
            if type(cb) is tuple:
                direction, cb = cb
                if len(cb) == 1:
                    return wrap(cb[0])
                if direction == '<':
                    return wrap(cb[-1], parent=wrap((direction, cb[:-1])))
                return wrap(cb[0], parent=wrap((direction, cb[1:])))

            def _cb(*args, **kwargs):
                extra_kwargs = result.copy()
                extra_kwargs.update(kwargs)
                out = cb(*args, **extra_kwargs)
                if parent is not None:
                    extra_kwargs['caller'] = lambda: out
                    out = parent(*args, **extra_kwargs)
                return out

            return _cb

        result.update({'compo': self,
                       'container': self.get_themed_template(env, 'container'),
                       'row': self.get_themed_template(env, 'row'),
                       'before': self.get_themed_template(env, 'before'),
                       'after': self.get_themed_template(env, 'after')})
        result['container'] = wrap(result['container'])
        result['row'] = wrap(result['row'])
        result['before'] = wrap(result['before'])
        result['after'] = wrap(result['after'])
        return result

    def after_event_handling(self):
        """
        After all events have been handled :meth:`update_children` is executed once for components that follow
        the :meth:`get_data` pattern.
        """
        super(ComponentContainerBase, self).after_event_handling()
        if self.auto_update_children:
            self.update_children(force=True)

    def is_smart(self):
        """Returns true if component uses get_data scheme."""
        return self.default_child_cls is not None

    @profile
    def update_children(self, force=False, init_transaction=False):
        """If a default_child_cls has been set this updates all child components to reflect the current state from
        get_data(). Will raise an exception if called twice without the force parameter present."""

        if self.__update_children_done__ and not force:
            raise Exception('update_children called twice without force parameter for component %s.' % self.cid)
        self.__update_children_done__ = True

        if not self.is_smart():
            return

        data = self._get_data(self.row_offset, self.row_limit, self.row_data)

        tipping_point = len([c for c in self.components if not hasattr(c, 'id')])

        current_order = []
        new_order = []

        data_dict = {}
        data_cid_dict = {}

        for v in self.components:
            if getattr(v, 'id', None) is None:
                continue
            current_order.append(v.id)
            data_cid_dict[v.id] = v.cid

        for i, d in enumerate(data):
            new_order.append(d['id'])
            data_dict[d['id']] = d

        # IDs of components no longer present in data. Their matching components are deleted.
        for data_id in set(current_order).difference(new_order):
            self.del_component(data_cid_dict.pop(data_id))
            self.redraw()

        # IDs of data not yet represented by a component. Matching components are created.
        for data_id in set(new_order).difference(current_order):
            data_cid_dict[data_id] = self.add_component(self.default_child_cls(**data_dict[data_id]),
                                                        init_transaction=init_transaction).cid
            self.redraw()

        # IDs of data represented by a component. Matching components are updated.
        for data_id in set(new_order).intersection(current_order):
            compo = getattr(self.page, data_cid_dict[data_id])
            for k, v in data_dict[data_id].items():
                if getattr(compo, k) != v:
                    setattr(compo, k, v)
                    self.redraw()

        # Rebuild order.
        for i, data_id in enumerate(new_order):
            try:
                if self.components[i + tipping_point].id != data_id:
                    self.switch_component(self.cid, data_cid_dict[data_id], position=i + tipping_point)
                    self.redraw()
            except AttributeError:
                pass

    def _get_data(self, *args, **kwargs):
        """
        Internal wrapper for :meth:`get_data` to decide wether it is to be called as a function or only contains a
        reference to a model on :attr:`.epflpage.Page.model`.
        """
        if type(self.get_data) is str and self.page.model is not None:
            return self.page.model.get(self, self.get_data, (args, kwargs), self.data_interface)
        elif type(self.get_data) is tuple and self.page.model is not None:
            return self.page.model[self.get_data[0]].get(self, self.get_data[1], (args, kwargs), self.data_interface)
        return self.get_data(*args, **kwargs)

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        """ Overwrite this method to automatically provide data to this components children.

        The list must comprise of dict like data objects with an id key. The data objects will be used as parameters for
        the creation of a default_child_cls component.

        May also be overwritten with a method selector string linking to a load\_ method of a page model or a tuple
        containing a model selector and a method selector.
        """
        return []

    def handle_set_row(self, row_offset, row_limit, row_data=None):
        """
        Default handler to deal with setting row offset, limit and data parameters.
        """
        self.row_offset, self.row_limit, self.row_data = row_offset, row_limit, row_data

    def init_struct(self):
        """
        Called before the :attr:`node_list` is used to create the sub structures of this component.
        """
        pass

    def init_transaction(self):
        """
        Components derived from :class:`ComponentContainerBase` will use their :attr:`node_list` to generate their
        children automatically. After initial setup :meth:`update_children` is executed once for components that follow
        the :meth:`get_data` pattern.
        """
        super(ComponentContainerBase, self).init_transaction()

        self.node_list = self.init_struct() or self.node_list  # if init_struct returns None, keep original value.

        for node in self.node_list:
            cid, slot = node.position

            compo = self.add_component(node(self.page, cid, __instantiate__=True),
                                       slot=slot,
                                       cid=cid,
                                       init_transaction=True)

        if self.auto_initialize_children:
            self.update_children(force=True, init_transaction=True)

    def replace_component(self, old_compo_obj, new_compo_obj):
        """Replace a component with a new one. Handles deletion bot keeping position and cid the same."""
        cid = old_compo_obj.cid
        position = self.components.index(old_compo_obj)
        old_compo_obj.delete_component()
        return self.add_component(new_compo_obj(cid=cid), position=position)

    @profile
    def add_component(self, compo_obj, slot=None, cid=None, position=None, init_transaction=False):
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

        compo_obj.register_in_transaction(self, slot, position=position)

        # handle the static part
        self.page.add_static_component(cid, compo_obj)

        # the transaction-setup has to be redone because the component can
        # directly be displayed in this request.
        if init_transaction is False:
            self.page.handle_transaction()
        else:
            compo_obj.init_transaction()

        return compo_obj

    def setup_component_slots(self):
        """ Overwrite me. This method must initialize the slots that this
        container-component provides to accumulate components """
        self.components = ComponentList(self)

    def add_component_to_slot(self, compo_obj, slot, position=None):
        """ This method must fill the correct slot with the component """
        if position is not None:
            self.components.insert(position, compo_obj)
        else:
            self.components.append(compo_obj)

    def del_component(self, compo_obj, slot=None):
        """
        Removes the component from the slot and form the compo_info. Accepts either a component instance or a cid.
        """
        if type(compo_obj) is str:
            return getattr(self.page, compo_obj).delete_component()

        compo_obj.compo_destruct()
        if hasattr(compo_obj, 'components'):
            for compo in list(compo_obj.components):
                compo.delete_component()


class ComponentList(MutableSequence):
    """

    """

    def __init__(self, container_compo):
        self.container_compo = container_compo

    def __setitem__(self, index, value):
        pass

    def insert(self, index, value):
        pass

    def __len__(self):
        return len(self.container_compo.struct_dict)

    def __getitem__(self, index):
        cid = self.container_compo.struct_dict.keys()[index]
        return getattr(self.container_compo.page, cid)

    def __delitem__(self, index):
        pass
