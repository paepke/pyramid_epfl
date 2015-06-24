from pyramid import testing
import pytest

from solute.epfl import get_epfl_jinja2_environment, includeme
from pyramid_jinja2 import get_jinja2_environment


class DummyRoute(object):
    def __init__(self, name='dummy_route'):
        self.name = name


@pytest.fixture(scope='session')
def route():
    return DummyRoute()


@pytest.fixture(scope='session')
def pyramid_req(route):
    config = testing.setUp()

    testing.DummyRequest.get_jinja2_environment = get_jinja2_environment
    testing.DummyRequest.get_epfl_jinja2_environment = get_epfl_jinja2_environment
    
    includeme(config)

    r = testing.DummyRequest()
    r.matched_route = route
    r.content_type = ''
    r.is_xhr = False
    r.registry.settings['epfl.transaction.store'] = 'memory'

    return r