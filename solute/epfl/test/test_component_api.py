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


@pytest.fixture(params=['static', 'static_with_child', 'static_as_child', 'dynamic', 'dynamic_with_child'])
def container_type(request, page, component_container_type_class):
    root_node = ComponentContainerBase
    if request.param == 'static':
        root_node = component_container_type_class()
    elif request.param == 'static_with_child':
        root_node = component_container_type_class(
            node_list=[ComponentBase(cid='child_compo')]
        )
    elif request.param == 'static_as_child':
        root_node = ComponentContainerBase(
            node_list=[
                component_container_type_class(cid='tested_component')
            ])

    page.root_node = root_node
    page.handle_transaction()

    if request.param == 'dynamic':
        page.root_node.add_component(
            component_container_type_class(cid='tested_component')
        )
    elif request.param == 'dynamic_with_child':
        page.root_node.add_component(
            component_container_type_class(
                cid='tested_component',
                node_list=[ComponentBase()]
            ))

    try:
        return page, page.tested_component, page.transaction.get_component('tested_component')
    except AttributeError:
        return page, page.root_node, page.transaction.get_component('root_node')


def test_base_type(base_type, result):
    page, tested_node, compo_info = base_type

    assert_coherence(tested_node, compo_info, result)

    rendered_html = page.root_node.render()
    rendered_js = page.root_node.render(target='js')

    assert_rendering(compo_info, rendered_html, rendered_js, result)


def test_base_type_style(component_base_type_class, result):
    assert_style(component_base_type_class, result)


def test_container_type(container_type, result):
    page, tested_node, compo_info = container_type

    assert_coherence(tested_node, compo_info, result)

    rendered_html = page.root_node.render()
    rendered_js = page.root_node.render(target='js')

    assert_rendering(compo_info, rendered_html, rendered_js, result)


def test_container_type_style(component_container_type_class, result):
    assert_style(component_container_type_class, result)


