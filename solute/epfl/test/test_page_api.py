import time

from solute.epfl.core.epflpage import Page
from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.core.epflcomponentbase import ComponentContainerBase
from solute.epfl import components

from collections2.dicts import OrderedDict
import inspect

from fixtures import pyramid_req
import pytest


class TestPageApi(object):
    def __init__(self):
        super(TestPageApi, self).__init__()

    def test_basic_component_operations(self, pyramid_req):
        page = Page(pyramid_req)
        t = page.transaction

        page.root_node = ComponentContainerBase
        page.handle_transaction()
        assert t.has_component('root_node')

        page.root_node.add_component(ComponentBase(cid='child_node',
                                                   compo_state=['test'],
                                                   test=None))

        assert t.has_component('child_node')

    def test_basic_component_regeneration(self, pyramid_req):
        page = Page(pyramid_req)
        page.root_node = ComponentContainerBase
        t = page.transaction
        t['components_assigned'] = True

        t.set_component('root_node', {'cid': 'root_node',
                                      'slot': None,
                                      'config': {},
                                      'class': (ComponentContainerBase,
                                                {},
                                                ('27a3d2ef7f76417bb2ebde9853f0c2a6', None))})

        t.set_component('child_node', {'slot': None,
                                       'ccid': 'root_node',
                                       'config': {'test': None,
                                                  'compo_state': ['test']},
                                       'class': (ComponentBase,
                                                 {'test': None,
                                                  'compo_state': ['test']},
                                                 ('child_node', None)),
                                       'cid': 'child_node',
                                       'compo_state': {'test': 'foobar'}})

        page.handle_transaction()

        assert page.root_node is not None and page.child_node is not None
        assert page.child_node.test == 'foobar'

        page.child_node.test = {'some': 'dict'}

        assert t.get_component('child_node')['compo_state']['test'] == {'some': 'dict'}

        new_page = Page(pyramid_req, transaction=t)
        new_page.handle_transaction()

        assert t.get_component('child_node')['compo_state']['test'] == {'some': 'dict'}
        assert new_page.child_node.test == {'some': 'dict'}

    def test_component_regeneration_performance(self, pyramid_req):
        page = Page(pyramid_req)
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})
        transaction.set_component('child_node_0',
                                  {'ccid': 'root_node',
                                   'cid': 'child_node_0',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('child_node_0', None))})

        compo_depth = 50
        compo_width = 100

        steps = [time.time()]
        for i in range(0, compo_depth):
            transaction.set_component('child_node_%s' % (i + 1),
                                      {'ccid': 'child_node_%s' % i,
                                       'cid': 'child_node_%s' % (i + 1),
                                       'slot': None,
                                       'config': {},
                                       'class': (ComponentContainerBase,
                                                 {},
                                                 ('child_node_%s' % (i + 1), None))})
            for x in range(0, compo_width):
                transaction.set_component('child_node_%s_%s' % (i + 1, x),
                                          {'ccid': 'child_node_%s' % i,
                                           'cid': 'child_node_%s_%s' % (i + 1, x),
                                           'slot': None,
                                           'config': {},
                                           'class': (ComponentContainerBase,
                                                     {},
                                                     ('child_node_%s_%s' % (i + 1, x), None))})
        steps.append(time.time())

        page.handle_transaction()
        steps.append(time.time())

        assert (steps[-1] - steps[-2]) * 1. / compo_depth / compo_width < 1. / 5000

    def test_component_rendering_ajax(self, pyramid_req):

        page = Page(pyramid_req)
        page.request.is_xhr = True
        page.page_request.params = {"q": []}
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})

        page.handle_transaction()

        # import sys
        # base_components = int(sys.original_args[1])
        # leaf_components = int(sys.original_args[2])
        base_components = 10
        leaf_components = 200

        page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))
        for i in range(0, base_components):
            getattr(page, 'child_node_%s' % i) \
                .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
            for x in range(0, leaf_components):
                getattr(page,
                        'child_node_%s' % (i + 1)) \
                    .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))

        page.root_node.redraw()

        page.handle_ajax_events()

        assert True not in [c.is_rendered for c in page.get_active_components()]

        # start_time = time.time()
        out = page.render()
        # print base_components, leaf_components, int((time.time() - start_time) * 1000000)

        for i in range(0, base_components):
            assert ('epfl.set_component_info(\\"child_node_%s\\", \\"handle\\", [\'reinitialize\', \'set_row\']);' %
                    (i + 1)) in out, "Missing set component info for child_node_%s" % (i + 1)
            out = out.replace('epfl.set_component_info("child_node_%s", "handle", [\'set_row\']);' % (i + 1), '')
            for x in range(0, leaf_components):
                assert ('epfl.set_component_info(\\"child_node_%s_%s\\", \\"handle\\", [\'reinitialize\', '
                        '\'set_row\']);' % (i + 1, x)) in out
                out = out.replace('epfl.set_component_info("child_node_%s_%s", "handle", [\'set_row\']);' % (i + 1, x),
                                  '')
        assert 'epfl.set_component_info(\\"child_node_0\\", \\"handle\\", [\'reinitialize\', \'set_row\']);' \
               'epfl.set_component_info(\\"root_node\\", \\"handle\\", [\'reinitialize\', \'set_row\']);' in out

    def test_component_deletion_and_recreation(self, pyramid_req):
        page = Page(pyramid_req)
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})

        page.handle_transaction()

        def create_child_components():
            page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))
            for i in range(0, 10):
                getattr(page, 'child_node_%s' % i) \
                    .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
                for x in range(0, 3):
                    getattr(page,
                            'child_node_%s' % (i + 1)) \
                        .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))

        create_child_components()

        assert len(page.root_node.components) == 1
        page.child_node_0.delete_component()

        assert transaction['compo_lookup'] == {}
        assert transaction.get_component('root_node') == {'cid': 'root_node',
                                                          'compo_struct': OrderedDict(),
                                                          'slot': None,
                                                          'config': {},
                                                          'class': (ComponentContainerBase,
                                                                    {},
                                                                    ('root_node', None))}
        assert len(page.root_node.components) == 0
        create_child_components()
        assert len(page.root_node.components) == 1

        assert len(transaction['compo_lookup']) == 41
        assert page.child_node_4_1

    def test_component_deletion(self, pyramid_req):
        page = Page(pyramid_req)
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})

        page.handle_transaction()

        page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))

        for i in range(0, 10):
            getattr(page, 'child_node_%s' % i) \
                .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
            getattr(page, 'child_node_%s' % (i + 1))
            for x in range(0, 3):
                getattr(page,
                        'child_node_%s' % (i + 1)) \
                    .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))
                getattr(page, 'child_node_%s_%s' % (i + 1, x))

        page.child_node_0.delete_component()

        assert transaction.has_component('child_node_0') is False
        for i in range(0, 10):
            assert transaction.has_component('child_node_%s' % (i + 1)) is False
            for x in range(0, 3):
                assert transaction.has_component('child_node_%s_%s' % (i + 1, x)) is False

    def test_re_rendering_components(self, pyramid_req):
        page = Page(pyramid_req)
        page.request.is_xhr = True
        page.page_request.params = {"q": []}
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})
        transaction.set_component('child_node_0',
                                  {'ccid': 'root_node',
                                   'cid': 'child_node_0',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('child_node_0', None))})

        compo_depth = 5
        compo_width = 10

        for i in range(0, compo_depth):
            transaction.set_component('child_node_%s' % (i + 1),
                                      {'ccid': 'child_node_%s' % i,
                                       'cid': 'child_node_%s' % (i + 1),
                                       'slot': None,
                                       'config': {},
                                       'class': (ComponentContainerBase,
                                                 {},
                                                 ('child_node_%s' % (i + 1), None))})
            for x in range(0, compo_width):
                transaction.set_component('child_node_%s_%s' % (i + 1, x),
                                          {'ccid': 'child_node_%s' % i,
                                           'cid': 'child_node_%s_%s' % (i + 1, x),
                                           'slot': None,
                                           'config': {},
                                           'class': (ComponentContainerBase,
                                                     {},
                                                     ('child_node_%s_%s' % (i + 1, x), None))})

        page.handle_transaction()

        page.root_node.redraw()
        page.child_node_3_1.redraw()

        page.handle_ajax_events()

        out = page.render()

        for i in range(0, compo_depth):
            assert out.count(
                "epfl.replace_component('child_node_%s'" % (i + 1)
            ) == out.count("epfl.replace_component('child_node_0'")
            for x in range(0, compo_width):
                assert out.count(
                    "epfl.replace_component('child_node_%s_%s'" % (i + 1, x)
                ) == out.count("epfl.replace_component('child_node_0'")

    def test_container_assign(self, pyramid_req):
        Page.root_node = ComponentContainerBase(
            cid='root_node',
            node_list=[
                ComponentContainerBase(
                    cid='container_1',
                    node_list=[
                        ComponentBase(cid='compo_1')
                    ]
                ),
                ComponentContainerBase(
                    cid='container_2',
                    node_list=[
                        ComponentBase(cid='compo_2')
                    ]
                ),
                ComponentContainerBase(
                    cid='container_3',
                    node_list=[
                        ComponentBase(cid='compo_3')
                    ]
                ),
                ComponentContainerBase(
                    cid='container_4',
                    node_list=[
                        ComponentBase(cid='compo_4')
                    ]
                ),
            ]
        )

        page = Page(pyramid_req)

        page.handle_transaction()

        for compo in page.root_node.components:
            assert compo.cid[-2:] == compo.compo_info['compo_struct'].keys()[0][-2:]

    def test_documentation(self, pyramid_req):
        missing_docstring = 0
        missing_param_doc = 0
        missing_param_doc_absolute = 0
        errors = []
        methods = inspect.getmembers(Page, inspect.ismethod)
        for name, method in methods:
            if not method.__doc__:
                errors.append('Page method "{name}" is missing docstring.'.format(
                    name=name
                ))
                missing_docstring += 1
                continue

            code = method.func_code
            var_names = code.co_varnames
            missing_param_doc_count = 0
            for var_name in var_names:
                if var_name in ['self', 'cls']:
                    continue
                if ":param {var_name}:" not in method.__doc__:
                    errors.append('Page method "{name}" is missing parameter "{var_name}" in docstring.'.format(
                        name=name,
                        var_name=var_name
                    ))
                missing_param_doc_count += 1

            if missing_param_doc_count > 0:
                missing_param_doc += 1
                missing_param_doc_absolute += missing_param_doc_count

        errors = '\n'.join(errors + [
            '{0}/{1} methods undocumented.'.format(
                missing_docstring,
                len(methods)
            ),
            '{0} methods with {1} undocumented parameters.'.format(
                missing_param_doc,
                missing_param_doc_absolute,
            )])

        assert len(errors) == 0, "\n" + errors