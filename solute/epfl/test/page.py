import unittest
import time
from pyramid import testing

from solute.epfl.core.epflpage import Page
from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.core.epflcomponentbase import ComponentContainerBase

from solute.epfl import get_epfl_jinja2_environment, includeme
from pyramid_jinja2 import get_jinja2_environment

from collections2.dicts import OrderedDict


class PageTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        testing.DummyRequest.get_jinja2_environment = get_jinja2_environment
        testing.DummyRequest.get_epfl_jinja2_environment = get_epfl_jinja2_environment

        includeme(self.config)

        self.request = testing.DummyRequest()
        self.request.content_type = ''
        self.request.is_xhr = False
        self.request.registry.settings['epfl.transaction.store'] = 'memory'

    def tearDown(self):
        testing.tearDown()

    def test_basic_component_operations(self):
        page = Page(self.request)
        t = page.transaction

        page.root_node = ComponentContainerBase(page, 'root_node', __instantiate__=True)
        assert t.has_component('root_node')

        page.root_node.add_component(ComponentBase(cid='child_node',
                                                   compo_state=['test'],
                                                   test=None))

        assert t.has_component('child_node')

    def test_basic_component_regeneration(self):
        page = Page(self.request)
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

        page.create_components()

        assert page.root_node is not None and page.child_node is not None
        assert page.child_node.test == 'foobar'

        page.child_node.test = {'some': 'dict'}

        assert t.get_component('child_node')['compo_state']['test'] == {'some': 'dict'}

        new_page = Page(self.request, transaction=t)
        new_page.create_components()

        assert t.get_component('child_node')['compo_state']['test'] == {'some': 'dict'}
        assert new_page.child_node.test == {'some': 'dict'}

    def test_component_regeneration_performance(self):
        page = Page(self.request)
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

        page.create_components()
        steps.append(time.time())

        assert (steps[-1] - steps[-2]) * 1. / compo_depth / compo_width < 1. / 5000

    def test_component_rendering_ajax(self):

        page = Page(self.request)
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

        page.create_components()

        page.root_node.add_component(ComponentContainerBase(cid='child_node_0'))
        for i in range(0, 10):
            getattr(page, 'child_node_%s' % i) \
                .add_component(ComponentContainerBase(cid='child_node_%s' % (i + 1)))
            for x in range(0, 3):
                getattr(page,
                        'child_node_%s' % (i + 1)) \
                    .add_component(ComponentContainerBase(cid='child_node_%s_%s' % (i + 1, x)))

        page.root_node.redraw()

        assert page.handle_ajax_request()
        assert False not in [c.is_rendered for c in page.get_active_components()]

        out = page.call_ajax()
        for i in range(0, 10):
            assert ('epfl.replace_component(\'child_node_%s\', {"js":""});' % (i + 1)) in out
            assert ('epfl.set_component_info("child_node_%s", "handle", [\'set_row\']);' % (i + 1)) in out
            out = out.replace('epfl.replace_component(\'child_node_%s\', {"js":""});' % (i + 1), '')
            out = out.replace('epfl.set_component_info("child_node_%s", "handle", [\'set_row\']);' % (i + 1), '')
            for x in range(0, 3):
                assert ('epfl.replace_component(\'child_node_%s_%s\', {"js":""});' % (i + 1, x)) in out
                assert ('epfl.set_component_info("child_node_%s_%s", "handle", [\'set_row\']);' % (i + 1, x)) in out
                out = out.replace('epfl.replace_component(\'child_node_%s_%s\', {"js":""});' % (i + 1, x), '')
                out = out.replace('epfl.set_component_info("child_node_%s_%s", "handle", [\'set_row\']);' % (i + 1, x),
                                  '')
        assert 'epfl.replace_component(\'child_node_0\', {"js":""});' \
               'epfl.set_component_info("child_node_0", "handle", [\'set_row\']);' \
               'epfl.set_component_info("root_node", "handle", [\'set_row\']);' in out

    def test_component_deletion_and_recreation(self):
        page = Page(self.request)
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})

        page.create_components()

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

    def test_component_deletion(self):
        page = Page(self.request)
        transaction = page.transaction
        transaction['components_assigned'] = True
        transaction.set_component('root_node',
                                  {'cid': 'root_node',
                                   'slot': None,
                                   'config': {},
                                   'class': (ComponentContainerBase,
                                             {},
                                             ('root_node', None))})

        page.create_components()

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
