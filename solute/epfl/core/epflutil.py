# coding: utf-8

import os, urllib, urlparse

from pyramid import security

from solute.epfl import json
from solute.epfl import core


class DictTransformer(object):

    def __init__(self, target_keys):
        self.target_keys = target_keys

    def __call__(self, data):
        out = {}
        for key in self.target_keys:
            out[key] = data[key]
        return out


class Dict2ListTransformer(object):

    def __init__(self, target_keys):
        self.target_keys = target_keys

    def __call__(self, data):
        out = []
        for key in self.target_keys:
            out.append(data[key])
        return out



def make_dict_transformer(target_keys):
    return DictTransformer(target_keys)

def make_dict2list_transformer(target_keys):
    return Dict2ListTransformer(target_keys)



class ClassAttributeExtender(type):

    def __new__(cls, name, bases, dct):
        print "Allocating memory for class", name
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        print "Init'ing (configuring) class", name
        super(ClassAttributeExtender, cls).__init__(name, bases, dct)



def add_extra_contents(response, obj):
    """ Adds CSS and JS extra-Contents of this object to the response.
    The object must have the following attributes:
    asset_spec
    js_name
    css_name
    """

    if obj.js_name:
        for js_name in obj.js_name:
            asset_spec = "{spec}/{name}".format(spec = obj.asset_spec, name = js_name)
            url = obj.request.static_url(asset_spec)
            js_script_src = core.epflclient.JSLink(url)
            response.add_extra_content(js_script_src)

    if obj.css_name:
        for css_name in obj.css_name:
            asset_spec = "{spec}/{name}".format(spec = obj.asset_spec, name = css_name)
            url = obj.request.static_url(asset_spec)
            js_script_src = core.epflclient.CSSLink(url)
            response.add_extra_content(js_script_src)


def get_page_class_by_name(request, page_name):
    """
    Given a page-name (the page.get_name()-result), it returns this page - or raises an error.
    todo: This needs some caching!
    """
    introspector = request.registry.introspector

    for intr in introspector.get_category("views"):
        view_callable = intr["introspectable"]["callable"]
        if type(view_callable) is type and issubclass(view_callable, core.epflpage.Page):
            if view_callable.get_name() == page_name:
                return view_callable

    raise ValueError, "Page '" + page_name + "' not found!"

def get_page_classes_from_route(request, route_name):
    """
    Given the request and a route-name, it collects all Page-Objects that are bound to this route.
    It returns a list of the page-classes.

    todo: This needs some caching!
    """
    introspector = request.registry.introspector

    candidates = []
    for intr in introspector.get_category("views"):
        if intr["introspectable"]["route_name"] == route_name:
            view_callable = intr["introspectable"]["callable"]
            if type(view_callable) is type and issubclass(view_callable, core.epflpage.Page):
                candidates.append(view_callable)

    return candidates


def has_permission_for_route(request, route_name, permission):
    """
    Given a request, a route-name and a permission, it checks, if the current user has this permission for at least
    one of the page-objects that are bound to this route.
    """

    page_objs = get_page_classes_from_route(request, route_name)

    for resource in page_objs:
        if not security.has_permission("access", resource, request):
            return False

    return True

def get_component(request, tid, cid):
    """
    If you do not have a page_obj (maybe you are in a pure pyramid-view-function), and you need a component,
    this is the function for you!
    """

    transaction = core.epfltransaction.Transaction(request, tid)
    page_name = transaction.get_page_name()
    page_class = get_page_class_by_name(request, page_name)
    page_obj = page_class(request, transaction)
    page_obj.setup_components()
    return page_obj.components[cid]

def get_widget(request, tid, cid, wid):
    """
    Same as get_component, but it returns a widget - in case the compo is a form!
    """
    compo_obj = get_component(request, tid, cid)
    return compo_obj.get_widget_by_wid(wid)




class URL(object):

    def __init__(self, url):
        self.parsed_url = urlparse.urlsplit(url)

    def update_query(self, **kwargs):
        qsl = urlparse.parse_qsl(self.parsed_url.query)
        for key, value in kwargs.items():
            qsl.append((key, value))
        new_url = urlparse.SplitResult(scheme = self.parsed_url.scheme,
                                       netloc = self.parsed_url.netloc,
                                       path = self.parsed_url.path,
                                       query = urllib.urlencode(qsl),
                                       fragment = self.parsed_url.fragment)

        return new_url.geturl()
