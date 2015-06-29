from pyramid import testing
import pytest
import inspect

from solute.epfl.core.epflcomponentbase import ComponentBase, ComponentContainerBase
from solute.epfl import get_epfl_jinja2_environment, includeme, epflpage, components
from pyramid_jinja2 import get_jinja2_environment


def is_container_compo(compo_name):
    if compo_name == 'ComponentBase':
        return False
    if compo_name == 'ComponentContainerBase':
        return True
    return issubclass(getattr(components, compo_name, None), ComponentContainerBase)


def pytest_cmdline_preparse(args):
    new_args = []
    for arg in args:
        if arg.startswith('--target='):
            target = arg[9:]

            if is_container_compo(target):
                new_args.extend([
                    "solute/epfl/test/test_component_api.py::test_container_type[%s-%s]" % (sub_target, target)
                    for sub_target in ['static', 'static_with_child', 'static_as_child', 'dynamic',
                                       'dynamic_with_child']
                ])
                new_args.append("solute/epfl/test/test_component_api.py::test_container_type_style[%s]" % target)
            else:
                new_args.extend([
                    "solute/epfl/test/test_component_api.py::test_base_type[%s-%s]" % (sub_target, target)
                    for sub_target in ['static', 'dynamic']
                ])
                new_args.append("solute/epfl/test/test_component_api.py::test_base_type_style[%s]" % target)

            continue

        new_args.append(arg)

    args[:] = new_args


@pytest.fixture(scope='session')
def result():
    """Fixture for controlling the overall state of tests in the current session.
    """

    return {'item_count': 0, 'objects_with_items': 0}


class DummyRoute(object):
    def __init__(self, name='dummy_route'):
        self.name = name


@pytest.fixture(scope='function')
def route():
    """Fixture to access a mocked (pyramid) route object.
    """
    return DummyRoute()


@pytest.fixture(scope='function')
def config():
    """Fixture to access a pyramid mock config.
    """
    return testing.setUp()


@pytest.fixture
def pyramid_req(route, config):
    """Fixture to access a pyramid mock request.

    :param route: Mocked route object.
    :param config: Mocked pyramid config.
    """
    testing.DummyRequest.get_jinja2_environment = get_jinja2_environment
    testing.DummyRequest.get_epfl_jinja2_environment = get_epfl_jinja2_environment

    includeme(config)

    config.add_route('dummy_route', pattern='/')

    r = testing.DummyRequest()
    r.matched_route = route
    r.content_type = ''
    r.is_xhr = False
    r.registry.settings['epfl.transaction.store'] = 'memory'

    return r


@pytest.fixture
def pyramid_xhr_req(pyramid_req):
    """Fixture to access a pyramid mock request setup like an AJAX request.

    :param pyramid_req: Mocked pyramid request.
    """
    pyramid_req.is_xhr = True
    return pyramid_req


@pytest.fixture
def page(pyramid_req):
    """Fixture to access a mocked EPFL Page setup with a pyramid mock request.

    :param pyramid_req: Mocked pyramid request.
    """
    return epflpage.Page(pyramid_req)


def component_base_type_predicate(cls):
    """Inspect predicate to select classes inheriting from ComponentBase but not from ComponentContainerBase.

    :param cls: Object to be inspected, must not necessarily be a class.
    """
    return inspect.isclass(cls) and issubclass(cls, ComponentBase) and not issubclass(cls, ComponentContainerBase)


def component_container_type_predicate(cls):
    """Inspect predicate to select classes inheriting from ComponentContainerBase.

    :param cls: Object to be inspected, must not necessarily be a class.
    """
    return inspect.isclass(cls) and issubclass(cls, ComponentContainerBase)


component_cls = inspect.getmembers(components, predicate=component_base_type_predicate) + [
    ('ComponentBase', ComponentBase)]


@pytest.fixture(params=component_cls, ids=[name for name, cls in component_cls])
def component_base_type_class(request):
    """Fixture to access all EPFL classes as defined by the component_base_type_predicate.

    :param request: py.test request object.
    """
    cls = request.param[1]
    return cls


component_container_cls = inspect.getmembers(components, predicate=component_container_type_predicate) + [
    ('ComponentContainerBase', ComponentContainerBase)]


@pytest.fixture(params=component_container_cls, ids=[name for name, cls in component_container_cls])
def component_container_type_class(request):
    """Fixture to access all EPFL classes as defined by the component_container_type_predicate.

    :param request: py.test request object.
    """
    cls = request.param[1]
    return cls
