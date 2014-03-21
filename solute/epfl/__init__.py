#* coding: utf-8

import os

import ujson as json # package abstraction

from solute.epfl.core.epflpage import Page # shortcut
from solute.epfl import fields # shortcut

import components
import widgets

from solute.epfl.jinja import jinja_reflection
from solute.epfl.jinja import jinja_extensions
from solute.epfl.jinja import jinja_helpers

from zope.interface import Interface

from solute.epfl.core import epfltransaction, epflutil


class IEPFLJinja2Environment(Interface):
    pass

class IEPFLGlobalData(Interface):
    pass


# handling extra data in different scopes:

def get_epfl_request_param(request, param_name, default = None):
    if not hasattr(request, "__epfl_params"):
        setattr(request, "__epfl_params", {})

    params = getattr(request, "__epfl_params")

    return params.get(param_name, default)

def set_epfl_request_param(request, param_name, value):
    if not hasattr(request, "__epfl_params"):
        setattr(request, "__epfl_params", {})

    params = getattr(request, "__epfl_params")
    params[param_name] = value

def get_epfl_global_param(request, param_name, default = None):

    gd = request.registry.queryUtility(IEPFLGlobalData)

    if gd is None:    
        return default

    return gd.get(param_name, default)

def set_epfl_global_param(request, param_name, value):

    gd = request.registry.queryUtility(IEPFLGlobalData)

    if gd is None:    
        gd = {}

    gd[param_name] = value

    request.registry.registerUtility(gd, IEPFLGlobalData)



# other stuff

def register_template_usage(request, template_name, page_obj):
    """
    The framework needs to know the page object and it's used template for this request.
    """
    pass # todo


#synchronized
def get_transaction(request):
    transaction = request.get_epfl_request_param("transaction")

    if not transaction:
        transaction = epfltransaction.Transaction(request)
        request.set_epfl_request_param("transaction", transaction)

    return transaction

def get_transaction_id(request):

    if request.is_xhr:
        return request.json_body["tid"]
    elif "__tid__" in request.params:
        return request.params["__tid__"]
    else:
        return request.get_epfl_request_param("tid")

def set_transaction_id(request, tid):
    request.set_epfl_request_param("tid", tid)


def get_epfl_jinja2_environment(request):
    """ This creates a jinja2-environment specific to use with epfl.
    It uses the needed special environment-classes and template-loaders.
    It copies the configuration from the "original"-pyramid-jinja2-environment.
    Safe to call multiple times.
    """

    environment = request.registry.queryUtility(IEPFLJinja2Environment)
    if environment is not None:
        return environment

    oenv = request.get_jinja2_environment()

    loader = jinja_helpers.PreprocessingFileSystemLoader(oenv.loader.searchpath,
                                                         encoding = oenv.loader.encoding,
                                                         debug = oenv.loader.debug)

    cache_size = int(request.registry.settings.get("jinja2.cache_size", 50))

    env = jinja_reflection.ReflectiveEnvironment(loader = loader,
                                                 auto_reload = oenv.auto_reload,
                                                 extensions = oenv.extensions,
                                                 undefined = oenv.undefined,

                                                 block_start_string = oenv.block_start_string,
                                                 block_end_string = oenv.block_end_string,
                                                 variable_start_string = oenv.variable_start_string,
                                                 variable_end_string = oenv.variable_end_string,
                                                 comment_start_string = oenv.comment_start_string,
                                                 comment_end_string = oenv.comment_end_string,
                                                 line_statement_prefix = oenv.line_statement_prefix,
                                                 line_comment_prefix = oenv.line_comment_prefix,
                                                 trim_blocks = oenv.trim_blocks,
                                                 lstrip_blocks = oenv.lstrip_blocks,
                                                 newline_sequence = oenv.newline_sequence,
                                                 keep_trailing_newline = oenv.keep_trailing_newline,
                                                 optimized = oenv.optimized,
                                                 finalize = oenv.finalize,
                                                 autoescape = oenv.autoescape,
                                                 cache_size = cache_size,
                                                 bytecode_cache = oenv.bytecode_cache)

    # really shared!
    env.filters = oenv.filters
    env.globals = oenv.globals

    jinja_extensions.extend_environment(env)

    request.registry.registerUtility(env, IEPFLJinja2Environment)
    return request.registry.queryUtility(IEPFLJinja2Environment)

def is_template_marked_as_not_found(request, template_name):

    nfts = get_epfl_global_param(request, "not_found_templates", set())

    return template_name in nfts


def mark_template_as_not_found(request, template_name):

    nfts = get_epfl_global_param(request, "not_found_templates", set())
    nfts.add(template_name)
    set_epfl_global_param(request, "not_found_templates", nfts)


def includeme(config):
<<<<<<< HEAD
    """
    The main configuration of the EPFL
    """

    config.include('pyramid_jinja2')

    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')
    config.add_request_method(config.get_jinja2_environment)
    config.add_request_method(get_epfl_jinja2_environment)
    config.add_request_method(register_template_usage)
    config.add_request_method(get_transaction)
    config.add_request_method(get_transaction_id)
    config.add_request_method(set_transaction_id)
    config.add_request_method(set_epfl_request_param)
    config.add_request_method(get_epfl_request_param)
    config.add_request_method(is_template_marked_as_not_found)
    config.add_request_method(mark_template_as_not_found)

    config.add_jinja2_search_path("solute.epfl:templates")
    config.add_jinja2_search_path("solute.epfl.components:")
    config.add_jinja2_search_path("solute.epfl.widgets:")

    # static routes
    config.add_static_view(name = "epfl/static", path = "solute.epfl:static")
    components.add_static_routes(config)
    widgets.add_static_routes(config)

    
    

