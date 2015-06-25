import pytest
from solute.epfl import components

from link_asserts import assert_href_is, assert_with_a_twist


@pytest.fixture(params=[
    # event_name, route, url
    (None, None, None),
    ('some_event', None, None),
    ('some_event', 'some_route', None),
    ('some_event', 'some_route', 'some_url'),
    (None, '/test_link_route', None),
    (None, '/test_link_route', 'some_url'),
    (None, None, 'some_url'),
])
def link_param_url(request):
    return request.param + ('some text', None)


def test_name_generation(page):
    test_name = '[[{{test_name}}]]'
    test_text = '[[{{test_text}}]]'

    page.root_node = components.Link(
        url='/foobar'
    )
    page.handle_transaction()
    compo = page.root_node

    assert 'None' in compo.render(), 'text and name are not set, but "None" is missing in the rendered html.'
    compo.render_cache = None

    compo.text = test_text
    assert test_text in compo.render(), 'text set to "{text}" but is missing in the rendered html.'.format(
        text=test_text
    )
    compo.render_cache = None

    compo.text = test_text
    compo.name = test_name
    assert test_name in compo.render(), 'name set to "{name}" but is missing in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    assert test_text not in compo.render(), 'name set to "{name}" but text "{text}" is in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    compo.render_cache = None

    compo.text = None
    compo.name = test_name
    assert test_name in compo.render(), 'name set to "{name}" but is missing in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    assert 'None' not in compo.render(), 'name set to "{name}" but "None" is in the rendered html.'.format(
        text=test_text,
        name=test_name,
    )
    compo.render_cache = None


def test_url_generation(link_param_url, page, config):
    config.add_route('/test_link_route', pattern='/test_link_route')
    event_name, route, url, text, name = link_param_url

    page.root_node = components.Link(
        url=url,
        route=route,
        name=name,
        text=text,
        event_name=event_name,
    )
    page.handle_transaction()

    params = dict(
        _url=page.root_node._url,
        url=url,
        route=route,
        name=name,
        text=text,
        event_name=event_name,
    )

    compo = page.root_node

    if event_name:
        assert compo._url is None, 'event_name is set to {event_name} but _url is {_url}.'.format(**params)
        assert_href_is('event_name', params, compo, None)
    elif route:
        assert compo._url == route, 'route is set to {route} but _url is {_url}.'.format(**params)
        assert_href_is('route', params, compo, route)
    elif url:
        assert compo._url == url, 'url is set to {url} but _url is {_url}.'.format(**params)
        assert_href_is('url', params, compo, url)


def test_url_generation_with_dynamic_route(page, config):
    route = 'test_link_route_parametrized'
    config.add_route(route, pattern='/test_link_route/{param}')

    page.root_node = components.Link(
        text='foobar',
        route=route
    )
    page.handle_transaction()

    assert_href_is('route', {'route': route}, page.root_node, None)
    page.request.matchdict['param'] = '1234'
    assert_href_is('route', {'route': route}, page.root_node, '/test_link_route/1234')


def test_url_generation_with_dynamic_url(page):
    url = 'some_url/{with_a_twist}'
    page.root_node = components.Link(
        text='foobar',
        url=url
    )
    page.handle_transaction()

    assert_href_is('url', {'url': url}, page.root_node, None)
    twisted_url = assert_with_a_twist('url', page, url)
    assert_href_is('url', {'url': twisted_url}, page.root_node, twisted_url)
