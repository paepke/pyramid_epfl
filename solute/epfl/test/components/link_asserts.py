

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