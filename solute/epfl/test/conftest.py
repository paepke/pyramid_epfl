from pyramid import testing
import pytest
import inspect

from solute.epfl.core.epflcomponentbase import ComponentBase, ComponentContainerBase
from solute.epfl import get_epfl_jinja2_environment, includeme, epflpage, components
from pyramid_jinja2 import get_jinja2_environment


def pytest_addoption(parser):
    parser.addoption("--target", action="store", default="all", help="Choose a specific class to test.")


@pytest.fixture(scope='session')
def result():
    """Fixture for controlling the overall state of tests in the current session.
    """

    return {'item_count': 0, 'objects_with_items': 0}


@pytest.fixture
def target(request):
    """Fixture to access the target commandline option.
    """
    return request.config.getoption("--target")


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
def component_base_type_class(request, target):
    """Fixture to access all EPFL classes as defined by the component_base_type_predicate and not excluded by the target
       commandline option.

    :param request: py.test request object.
    :param target: Fixture for the target commandline option.
    """
    cls = request.param[1]
    if target != 'all' and target != cls.__name__:
        pytest.skip("Class name mismatch.")
    return cls


component_container_cls = inspect.getmembers(components, predicate=component_container_type_predicate) + [
    ('ComponentContainerBase', ComponentContainerBase)]

@pytest.fixture(params=component_container_cls, ids=[name for name, cls in component_container_cls])
def component_container_type_class(request, target):
    """Fixture to access all EPFL classes as defined by the component_container_type_predicate and not excluded by the
       target commandline option.

    :param request: py.test request object.
    :param target: Fixture for the target commandline option.
    """
    cls = request.param[1]
    if target != 'all' and target != cls.__name__:
        pytest.skip("Class name mismatch.")
    return cls
