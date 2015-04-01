import unittest
from pyramid import testing
import solute.epfl as epfl
import pyramid_jinja2
import inspect
import os


class ComponentBaseTest(unittest.TestCase):
    component = epfl.core.epflcomponentbase.ComponentBase

    def setUp(self):
        self.config = testing.setUp()
        testing.DummyRequest.get_jinja2_environment = pyramid_jinja2.get_jinja2_environment
        testing.DummyRequest.get_epfl_jinja2_environment = epfl.get_epfl_jinja2_environment

        epfl.includeme(self.config)

        self.request = testing.DummyRequest()
        self.request.content_type = ''
        self.request.is_xhr = False
        self.request.registry.settings['epfl.transaction.store'] = 'memory'

        self.page = epfl.core.epflpage.Page(self.request)
        self.transaction = self.page.transaction

    def tearDown(self):
        testing.tearDown()

    def test_static_component_rendering(self):
        self.run_test_component_creation_as_root_node(self.component)
        self.run_render_test_component_creation_as_root_node()

    def test_component_creation_as_root_node(self):
        self.run_test_component_creation_as_root_node(self.component)

    def test_component_creation_as_dynamic_node(self):
        self.run_test_component_creation_as_dynamic_node(self.component)

    def test_component_creation_as_dynamic_node_inside_dynamic_node(self):
        self.run_test_component_creation_as_dynamic_node_inside_dynamic_node(self.component)

    def run_render_test_component_creation_as_root_node(self):
        page = self.page
        root_node = page.root_node

        rendered_html = root_node.render()
        rendered_js = root_node.render(target='js')
        self.assert_rendered_html_base_parameters(rendered_html, 'root_node')
        self.assert_rendered_js_base_parameters(rendered_js)

    def run_test_component_creation_as_root_node(self, compo_class):
        page = self.page
        transaction = page.transaction

        page.root_node = compo_class
        page.setup_components()

        compo_info = transaction.get_component('root_node')
        page.root_node.set_visible()

        self.assert_component_base_properties(page.root_node, compo_info)

    def run_test_component_creation_as_dynamic_node_inside_dynamic_node(self, compo_class):
        page = self.page
        transaction = page.transaction

        page.root_node = epfl.core.epflcomponentbase.ComponentContainerBase
        page.setup_components()

        container_component = page.root_node.add_component(
            epfl.core.epflcomponentbase.ComponentContainerBase(cid='container_component')
        )

        container_component.add_component(compo_class(cid='tested_component'))

        compo_info = transaction.get_component('tested_component')
        self.assert_component_base_properties(page.tested_component, compo_info)

    def run_test_component_creation_as_dynamic_node(self, compo_class):
        page = self.page
        transaction = page.transaction

        page.root_node = epfl.core.epflcomponentbase.ComponentContainerBase
        page.setup_components()

        page.root_node.add_component(compo_class(cid='tested_component'))

        compo_info = transaction.get_component('tested_component')
        self.assert_component_base_properties(page.tested_component, compo_info)

    def assert_component_base_properties(self, component, compo_info):
        assert isinstance(component, epfl.core.epflcomponentbase.ComponentBase)

        if getattr(component, 'asset_spec', None) is not None:
            compo_name = component.__class__.__name__
            if ':{compo_name}/'.format(compo_name=compo_name.lower()) in component.asset_spec:
                file_path = inspect.getsourcefile(component.__class__)
                file_path = os.path.abspath(file_path)
                js_file_path = file_path[:-3] + '.js'

                package_path = os.path.dirname(file_path)

                static_path = package_path + '/static'
                static_js_file_path = static_path + '/{compo_name}.js'.format(compo_name=compo_name.lower())

                assert file_path.endswith(compo_name.lower() + '.py')
                assert package_path.endswith(compo_name.lower())
                assert os.path.exists(static_path)

                if os.path.exists(js_file_path):
                    js_file = file(js_file_path).read()
                    assert js_file.startswith('epfl.init_component("{{ compo.cid }}"')
                    assert js_file.startswith('epfl.init_component("{{ compo.cid }}", "%s", {' % compo_name)

                if os.path.exists(static_js_file_path):
                    js_file = file(static_js_file_path).read()
                    assert js_file.startswith("epfl.{compo_name} = function(cid, params) {".format(
                        compo_name=compo_name)
                    )

        assert component.slot == compo_info['slot']
        assert component.cid == compo_info['cid']
        assert component.__unbound_component__.__getstate__() == compo_info['class']

        assert component._ComponentBase__config == compo_info['config']

        for name in component.combined_compo_state:
            attr_value = getattr(component, name)
            setattr(component, name, attr_value)
            assert compo_info['compo_state'][name] == attr_value

    def assert_rendered_html_base_parameters(self, html, cid):
        assert html.count('epflid="{cid}"'.format(cid=cid)) == 1

    def assert_rendered_js_base_parameters(self, html):
        pass


class ComponentContainerBaseTest(ComponentBaseTest):
    component = epfl.core.epflcomponentbase.ComponentContainerBase
