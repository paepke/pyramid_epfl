test_venues = ['rendering', 'coherence', 'style']
test_scenarios = {
    'static': ['as', 'insertion_into_tested_compo', 'insertion_of_tested_compo'],
    'dynamic': ['as', 'insertion_into_tested_compo', 'insertion_of_tested_compo'],
    'recreation': ['as', 'insertion_into_tested_compo', 'insertion_of_tested_compo'],
}


def test_static_component_rendering(page, component_base_type_class):
    transaction = page.transaction

    page.root_node = component_base_type_class
    page.setup_components()

    compo_info = transaction.get_component('root_node')
    page.root_node.set_visible()

    assert_component_base_properties(page.root_node, compo_info)


def run_render_test_component_creation_as_root_node(self):
    page = self.page
    root_node = page.root_node

    rendered_html = root_node.render()
    rendered_js = root_node.render(target='js')
    self.assert_rendered_html_base_parameters(rendered_html, 'root_node')
    self.assert_rendered_js_base_parameters(rendered_js)


def assert_component_base_properties(component, compo_info):
    """Contains the following checks:
     * Coherence of object instance attributes to transaction compo_info.
     * Coherence of object instance compo_info to transaction compo_info.
     * Coherence and writability of object instance compo_state attributes into/to transaction compo_info.
    """
    assert component.slot == compo_info['slot'], "slot attribute differs in transaction and instance"
    assert component.cid == compo_info['cid'], "cid attribute differs in transaction and instance"
    assert component.__unbound_component__.__getstate__() == compo_info['class'], \
        "class attribute differs in transaction and instance"

    assert component._ComponentBase__config == compo_info['config'], "config not stored correctly in transaction"

    for name in component.combined_compo_state:
        attr_value = getattr(component, name)
        try:
            setattr(component, name, attr_value)
        except:
            import pdb

            pdb.set_trace()
            raise
        assert compo_info['compo_state'][name] == attr_value, \
            "compo_state not stored correctly for {name}. Should be {attr_value} actually is {state_value}".format(
                name=name,
                attr_value=attr_value,
                state_value=compo_info['compo_state'][name]
            )