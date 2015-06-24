import pytest
import re
import inspect
import os
from solute import epfl

from component_asserts import assert_coherence, assert_rendering, assert_style

from solute.epfl.core.epflcomponentbase import ComponentBase, ComponentContainerBase

test_venues = ['rendering', 'coherence', 'style']
dynamic_test_scenarios = ['as', 'insertion_into_tested_compo', 'insertion_of_tested_compo']


@pytest.fixture(params=['static', 'dynamic'])
def base_type(request, page, component_base_type_class):
    root_node = ComponentContainerBase
    if request.param == 'static':
        root_node = component_base_type_class

    transaction = page.transaction

    page.root_node = root_node
    page.handle_transaction()

    if request.param == 'static':
        compo_info = transaction.get_component('root_node')
        page.root_node.set_visible()
        tested_component = page.root_node
    else:
        page.root_node.add_component(component_base_type_class(cid='tested_component'))
        compo_info = transaction.get_component('tested_component')
        tested_component = page.tested_component

    return page, tested_component, compo_info


def test_base_type(base_type):
    page, tested_node, compo_info = base_type

    assert_coherence(tested_node, compo_info)

    rendered_html = page.root_node.render()
    rendered_js = page.root_node.render(target='js')

    assert_rendering(compo_info, rendered_html, rendered_js)


def test_base_type_style(component_base_type_class):
    assert_style(component_base_type_class)


