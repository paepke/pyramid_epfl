# coding: utf-8

from jinja2 import nodes
from jinja2 import Environment, PackageLoader, FileSystemLoader, StrictUndefined, Undefined
from jinja2.exceptions import UndefinedError, TemplateNotFound


"""
This module provides reflection for jinja templates.
It uses the parsed AST from the jinja-templates, so the reflection information is available before any rendering must occur.

It provides the information which part of the template uses which other part.
Currently Scopes (RIScope) and Usages (RIUsage) are used.
A scope is a macro-defintion, a call-block or a block.
A usage is the use of template-variables.

So for example the reflection-objects can tell you which macro "uses" a certain template-variable.

Use "ReflectiveEnvironment" as replacement for the jinja2-environment.
"""

class ReflectiveEnvironment(Environment):

    def __init__(self, *args, **kwargs):
        super(ReflectiveEnvironment, self).__init__(*args, **kwargs)

        self.reflection_info = {}

    def _parse(self, source, name, filename):
        """Internal parsing function used by `parse` and `compile`."""
        out = super(ReflectiveEnvironment, self)._parse(source, name, filename)

        self.reflection_info[name] = reflect(out)

        return out

    def get_reflection_info(self, template_obj):
        ri = self.reflection_info[template_obj.name]
        return ri


class RIScope(object):

    def __init__(self, typ, name, parent):
        self.typ = typ
        self.name = name
        self.parent = parent
        self.usages = []
        self.child_scopes = []
        self.sub_elements = []

        if parent:
            parent.child_scopes.append(self)
            parent.add_subelement(self)

    def add_usage(self, usage):
        self.usages.append(usage)
        usage.set_scope(self)
        self.add_subelement(usage)

    def add_subelement(self, el):
    	self.sub_elements.append(el)
    	if self.parent:
    		self.parent.add_subelement(el)

    def get_subelements(self):
    	return self.sub_elements

    def get_parent(self):
    	return self.parent

    def pprint(self, indent = 0):
        print "{indent}{name} ({typ}):".format(indent = (" " * indent), 
                                               name = self.name, 
                                               typ = self.typ)
        for usage in self.usages:
            usage.pprint(indent + 4)
        for sub_scope in self.child_scopes:
            sub_scope.pprint(indent + 4)

    def get_dotted(self):
    	return self.name

    def get_accessors(self):
    	return self.name, []


class RIUsage(object):

    def __init__(self, typ, keys):
        self.typ = typ
        self.keys = keys
        self.scope = None

    def set_scope(self, scope):
        self.scope = scope

    def get_dotted(self):
        return ".".join(self.keys)

    def pprint(self, indent = 0):
        print "{indent}{visual} ({typ})".format(indent = (" " * indent), 
                                                visual = self.get_dotted(), 
                                                typ = self.typ)

    def get_accessors(self):
    	return self.keys[0], self.keys[1:]

    def update_self_accessor(self, real_name):
        self.keys[0] = real_name

    def get_parent(self):
    	return self.scope



class ReflectionInfo(object):

    def __init__(self, doc):
        self.doc = doc
        self.page_obj_cache = {}

        self.root = RIScope("root", "root", None)
        self.parse(doc.body, self.root)

    def select_page(self, page_name):
        self.page_name = page_name

    def pprint(self):
        self.root.pprint()

    def _parse_getattr(self, node):
        out = []
        while True:
            if type(node) is nodes.Name:
                out.insert(0, node.name)
                break
            elif type(node) is nodes.Getattr:
                out.insert(0, node.attr)
                node = node.node
            else:
                break
        return out

    def _parse_call(self, call):

        call_args = []

        # the call object
        call_obj = self._parse_getattr(call.node)

        # the arguments
        for arg in call.args:
            args = self._parse_getattr(arg)
            if args:
                call_args.append(args)

        for arg in call.kwargs:
            args = self._parse_getattr(arg.value)
            if args:
                call_args.append(args)

        return call_obj, call_args


    def parse(self, all_nodes, scope):

        for node in all_nodes:

            new_scope = scope
            recurse_into = None

            if type(node) is nodes.Output:
                # recurse into the output
                recurse_into = node.nodes
            elif type(node) is nodes.Filter:
                usage = RIUsage("filter", [node.name])
                scope.add_usage(usage)
                call_obj, call_args = self._parse_call(node)
                for obj in [call_obj] + call_args:
                    usage = RIUsage("call", obj)
                    scope.add_usage(usage)
            elif type(node) is nodes.Macro:
                new_scope = RIScope("macro", node.name, scope)
                recurse_into = node.body
            elif type(node) is nodes.Block:
                new_scope = RIScope("block", node.name, scope)
                recurse_into = node.body
            elif type(node) is nodes.CallBlock:
                call_obj, call_args = self._parse_call(node.call)
                for obj in call_args:
                    usage = RIUsage("call", obj)
                    scope.add_usage(usage)
                usage = RIUsage("call", call_obj)
                scope.add_usage(usage)
                new_scope = RIScope("call_block", usage.get_dotted(), scope)
                recurse_into = node.body
            elif type(node) is nodes.Name:
                usage = RIUsage("obj", [node.name])
                scope.add_usage(usage)
            elif type(node) is nodes.Getattr:
                usage = RIUsage("obj", self._parse_getattr(node))
                scope.add_usage(usage)
            elif type(node) is nodes.Call:
                call_obj, call_args = self._parse_call(node)
                for obj in [call_obj] + call_args:
                    usage = RIUsage("call", obj)
                    scope.add_usage(usage)
            elif hasattr(node, "body"):
                recurse_into = node.body
            else:
            	pass
                #print "Unhandeled:", type(node)

            if recurse_into:
                self.parse(recurse_into, new_scope)

    def get_element_by_name(self, page_obj, name):
        """ Provide the EPFLPage and the fully qualified name (dotted) of the element you want to get the reflection-info.
        These are e.g. components and widgets.
        """
        page_name = page_obj.name
        if page_name not in self.page_obj_cache:
            self._generate_page_obj_cache(page_obj)

        return self.page_obj_cache[page_name].get(name, None)


    def _generate_page_obj_cache_walk_scope(self, scope, page_obj, cache, current_scope_obj_name):
        """ see _generate_page_obj_cache """

        if scope.name in page_obj.components:
            current_scope_obj_name = scope.name
            cache[scope.name] = scope

        for usage in scope.usages:
            obj = page_obj
            access_path = []
            access_path_template_element_idx = 0
            for key in usage.keys:
                if key == "self":
                    key = current_scope_obj_name
                    usage.update_self_accessor(key) # e.g. to change "self.macros.XXX" to "form.macros.XXX"

                obj = getattr(obj, key, None)
                access_path.append(key)
                if getattr(obj, "is_template_element", False):
                    access_path_template_element_idx = len(access_path)

            obj_name = ".".join(access_path[:access_path_template_element_idx])

            if obj_name not in cache:
                cache[obj_name] = usage

        for child_scope in scope.child_scopes:
            self._generate_page_obj_cache_walk_scope(child_scope, page_obj, cache, current_scope_obj_name)


    def _generate_page_obj_cache(self, page_obj):
        """ This cache translates the names of the components from the page_obj into it's representations
        of RIUsage or RIScope.
        It walks thourused in the templates (the names used in the curly-jinja2-braces) into the
        objects (tagged with is_template_element=True) available from the page_obj.
        This is neccessary because of constructs in the template like:

        {{ compo_obj.render() }}
        ->
        "compo_obj" is the name of the component that we are interested in!

        """
        page_name = page_obj.name
        cache = {} # this will map compo_name to it's RIUsage or RIScope
        self._generate_page_obj_cache_walk_scope(self.root, page_obj, cache, None)
        self.page_obj_cache[page_name] = cache



def reflect(doc):
    ri = ReflectionInfo(doc)
##    ri.pprint()
    return ri
