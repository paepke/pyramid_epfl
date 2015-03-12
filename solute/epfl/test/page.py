import unittest
import time
from pyramid import testing

from solute.epfl.core.epflpage import Page
from solute.epfl.core.epflcomponentbase import ComponentBase
from solute.epfl.core.epflcomponentbase import ComponentContainerBase


class PageTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
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
                                      'class': (ComponentContainerBase,
                                                {},
                                                ('27a3d2ef7f76417bb2ebde9853f0c2a6', None))})

        t.set_component('child_node', {'slot': None,
                                       'ccid': 'root_node',
                                       'class': (ComponentBase,
                                                 {'test': None,
                                                  'compo_state': ['test']},
                                                 ('child_node', None)),
                                       'cid': 'child_node',
                                       'compo_state': {'test': 'foobar'}})

        page.create_components()

        assert page.root_node is not None and page.child_node is not None
        assert page.child_node.test == 'foobar'
