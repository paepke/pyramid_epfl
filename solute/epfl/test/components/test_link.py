import pytest
from solute.epfl import components


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


def assert_with_a_twist(name, page, target_value):
    __tracebackhide__ = True

    with_a_twist = '1234'
    assert page.root_node._url is None, '{name} contains unset parameter "with_a_twist" but _url is {_url}'.format(
        _url=page.root_node._url,
        name=name,
    )

    page.request.matchdict['with_a_twist'] = with_a_twist
    assert page.root_node._url == target_value.format(with_a_twist=with_a_twist), \
        '{name} parameter "with_a_twist" set to {with_a_twist} but _url is {_url}'.format(
            with_a_twist=with_a_twist,
            _url=page.root_node._url,
            name=name,
        )

    return target_value.format(with_a_twist=with_a_twist)


def assert_href_is(name, params, compo, target_value):
    __tracebackhide__ = True

    errors = (
        '%s is set to {%s} but rendered html contains href.' % (name, name),
        '%s is set to {%s} but rendered html contains no href.' % (name, name),
        '%s is set to {%s} but rendered html contains wrong href.' % (name, name),
    )

    compo.render_cache = None

    if target_value is None:
        assert 'href=' not in compo.render(), errors[0].format(**params)
    else:
        assert 'href=' in compo.render(), errors[1].format(**params)
        assert 'href="{0}"'.format(target_value) in compo.render(), errors[2].format(**params)