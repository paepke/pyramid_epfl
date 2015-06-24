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

    def get_page_and_transaction(self):
        return self.page, self.page.transaction

    def bootstrap(self):
        page, transaction = self.get_page_and_transaction()
        page.root_node = self.component
        page.handle_transaction()
        return page, transaction

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
        page.handle_transaction()

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
        page.handle_transaction()

        page.root_node.add_component(compo_class(cid='tested_component'))

        compo_info = transaction.get_component('tested_component')
        self.assert_component_base_properties(page.tested_component, compo_info)

    def assert_component_base_properties(self, component, compo_info):
        assert isinstance(component, epfl.core.epflcomponentbase.ComponentBase),\
            "{compo} is not a {base_compo} instance.".format(
                compo=component, base_compo=epfl.core.epflcomponentbase.ComponentBase)

        assert component.slot == compo_info['slot'], "slot attribute differs in transaction and instance"
        assert component.cid == compo_info['cid'], "cid attribute differs in transaction and instance"
        assert component.__unbound_component__.__getstate__() == compo_info['class'],\
            "class attribute differs in transaction and instance"

        assert component._ComponentBase__config == compo_info['config'], \
            "config not stored correctly in transaction"

        for name in component.combined_compo_state:
            attr_value = getattr(component, name)
            setattr(component, name, attr_value)
            assert compo_info['compo_state'][name] == attr_value,\
                "compo_state not stored correctly for {name}. Should be {attr_value} actually is {state_value}".format(
                    name=name,
                    attr_value=attr_value,
                    state_value=compo_info['compo_state'][name]
                )

    def assert_rendered_html_base_parameters(self, html, cid):
        assert html.count('epflid="{cid}"'.format(cid=cid)) == 1, "element {cid} is missing".format(cid=cid)

    def assert_rendered_js_base_parameters(self, html):
        pass

    def test_class_attributes_and_scaffold_construction(self):
        import re

        component = self.component
        compo_name = component.__name__

        if getattr(component, 'asset_spec', None) is not None:
            if ':{compo_name}/'.format(compo_name=compo_name.lower()) in component.asset_spec:
                file_path = inspect.getsourcefile(component)
                file_path = os.path.abspath(file_path)
                js_file_path = file_path[:-3] + '.js'

                package_path = os.path.dirname(file_path)

                static_path = package_path + '/static'
                static_js_file_path = static_path + '/{compo_name}.js'.format(compo_name=compo_name.lower())

                assert file_path.endswith(compo_name.lower() + '.py'),\
                    "{compo_name} is missing primary python file.".format(compo_name=compo_name)
                assert package_path.endswith(compo_name.lower()),\
                    "{compo_name} has a malformed package path." \
                    " Should end with {compo_name_lower} actually is {package_path}".format(
                        compo_name=compo_name,
                        compo_name_lower=compo_name.lower(),
                        package_path=package_path,
                    )
                assert os.path.exists(static_path), "{compo_name} is missing static folder.".format(
                    compo_name=compo_name)

                if os.path.exists(js_file_path):
                    js_file = file(js_file_path).read()
                    assert js_file.startswith('epfl.init_component("{{ compo.cid }}"'),\
                        '{compo_name} has dynamic js missing \'epfl.init_component("{{{{ compo.cid }}}}"\''.format(
                            compo_name=compo_name)
                    assert js_file.startswith('epfl.init_component("{{ compo.cid }}", "%s", {' % compo_name),\
                        '{compo_name} has dynamic js missing ' \
                        '\'epfl.init_component("{{{{ compo.cid }}}}", "{compo_name}"\''.format(
                            compo_name=compo_name)
                if os.path.exists(static_js_file_path):
                    js_file = file(static_js_file_path).read()

                    r = re.compile("epfl\.{compo_name}\.inherits_from\(epfl\.([A-Za-z]*)\);".format(
                        compo_name=compo_name))
                    result = r.findall(js_file)
                    assert len(result) == 1,\
                        "{compo_name} is missing inheritance calls in static js.".format(compo_name=compo_name)
                    assert js_file.count("epfl.{base_compo}.call(this, cid, params);".format(base_compo=result[0])) == 1,\
                        "{compo_name} is missing inherited initiation call in static js. " \
                        "'epfl.{base_compo}.call(this, cid, params);' not found".format(
                            compo_name=compo_name, base_compo=result[0])

                    assert js_file.startswith("epfl.{compo_name} = function(cid, params) ".format(
                        compo_name=compo_name)),\
                        "{compo_name} is not correctly created in static js."
                    assert js_file.count("epfl.{compo_name}.inherits_from(epfl.".format(
                        compo_name=compo_name)) == 1,\
                        "{compo_name} is not correctly inheriting in static js."

        init_func = component.__init__
        init_docs = init_func.__doc__
        init_code = init_func.func_code
        assert init_docs, "{compo_name} __init__ method has no doc string.".format(compo_name=compo_name)
        if component not in [epfl.core.epflcomponentbase.ComponentBase,
                             epfl.core.epflcomponentbase.ComponentContainerBase]:
            # This parameter is not set in the ComponentBase, so it's only set
            # for custom __init__ methods that are required for all components
            assert 'page' in init_code.co_varnames,\
                "{compo_name} __init__ method is not correctly setup. " \
                "(Missing page parameter, or not overwritten.)".format(compo_name=compo_name)

            assert init_code.co_varnames[0] == 'self',\
                "{compo_name} __init__ method is missing or misplacing parameter 'self'.".format(compo_name=compo_name)
            assert init_code.co_varnames[1] == 'page',\
                "{compo_name} __init__ method is missing or misplacing parameter 'page'.".format(compo_name=compo_name)
            assert init_code.co_varnames[2] == 'cid',\
                "{compo_name} __init__ method is missing or misplacing parameter 'cid'.".format(compo_name=compo_name)
            assert init_code.co_varnames[-1] in ['extra_params', 'kwargs'],\
                "{compo_name} __init__ method is missing or misplacing parameter, 'extra_params' or 'kwargs'.".format(
                    compo_name=compo_name)

        for var in init_code.co_varnames:
            if var not in ['self', 'page', 'args', 'kwargs', 'extra_params', 'cid']:
                assert ":param {var}:".format(var=var) in init_docs,\
                    "{compo_name} __init__ method is missing docs for {param}.".format(compo_name=compo_name, param=var)

        source, starting_line = inspect.getsourcelines(self.component)

        custom_attributes = re.compile('^    [a-zA-Z_]* = .*$')
        doc_line = re.compile('^    #: .*$')
        for line_number, line in enumerate(source):
            abs_line_number = line_number + starting_line + 1
            search_result = custom_attributes.findall(line)
            if not search_result:
                continue
            attr_name = search_result[0].strip().split(' ', 1)[0]

            if attr_name in ['asset_spec', 'compo_state', 'theme_path', 'css_name', 'js_name', 'js_parts',
                             'new_style_compo', 'compo_js_params', 'compo_js_extras', 'compo_js_name', 'template_name',
                             'compo_config', 'data_interface', 'default_child_cls', 'auto_update_children',
                             'theme_path_default']:
                continue

            assert attr_name not in ['cid', 'slot'], "Invalid attribute set: 'slot' and 'cid' are reserved names." \
                                                     " (Line: {line_number})".format(line_number=abs_line_number)

            attr_tail = search_result[0].strip().split(' ', 2)[2]
            if '#' in attr_tail:
                assert '  #: ' in attr_tail,\
                    "Bad format on docstring for {attr_name}. Expected string containing '  #: ', got '{attr_tail}'" \
                    " instead. (Line: {line_number})".format(
                        attr_name=attr_name, attr_tail=attr_tail, line_number=abs_line_number)
                continue

            line_cursor = 1
            current_line = source[line_number - line_cursor]
            # No doc string yet, so look backwards.
            assert doc_line.match(current_line),\
                "No docstring found for {attr_name}. Expected a line starting with '#: ', got '{current_line}'" \
                " instead. (Line: {line_number})".format(
                    attr_name=attr_name, current_line=current_line.strip(), line_number=abs_line_number - line_cursor)

            while current_line.strip().startswith('#') and line_cursor <= current_line:
                assert doc_line.match(current_line),\
                    "Bad format docstring found for {attr_name}. Expected a line starting with '#: ', got " \
                    "'{current_line}' instead. (Line: {line_number})".format(
                        attr_name=attr_name, current_line=current_line.strip(),
                        line_number=abs_line_number - line_cursor)
                current_line = source[line_number - line_cursor]
                line_cursor += 1


class ComponentContainerBaseTest(ComponentBaseTest):
    component = epfl.core.epflcomponentbase.ComponentContainerBase

    def test_adding_and_deleting_components(self):
        page = self.page
        transaction = page.transaction

        page.root_node = self.component
        page.handle_transaction()

        root_node = page.root_node

        test_node_0 = root_node.add_component(epfl.core.epflcomponentbase.ComponentBase(
            cid='test_node_0'
        ), position=0)
        test_node_1 = root_node.add_component(epfl.core.epflcomponentbase.ComponentBase(
            cid='test_node_1',
            compo_state=['foobar'],
            foobar=None
        ), position=1)

        self.assert_component_base_properties(root_node, transaction.get_component('root_node'))
        self.assert_component_base_properties(test_node_0, transaction.get_component('test_node_0'))
        self.assert_component_base_properties(test_node_1, transaction.get_component('test_node_1'))

        test_node_0.delete_component()

        assert root_node.components[0] == test_node_1,\
            "{component} failed during deletion of child. (Wrong child found in position 1)".format(
                component=self.component)
        assert 'test_node_0' not in [compo.cid for compo in root_node.components],\
            "{component} failed during deletion of child. (Too many children left)".format(component=self.component)

    def test_rendering_sub_components(self):
        page = self.page
        transaction = page.transaction

        page.root_node = self.component
        page.handle_transaction()

        root_node = page.root_node

        test_node_0 = root_node.add_component(epfl.core.epflcomponentbase.ComponentBase(
            cid='test_node_0'
        ))
        test_node_1 = root_node.add_component(epfl.core.epflcomponentbase.ComponentBase(
            cid='test_node_1'
        ))

        rendered_html = root_node.render()
        rendered_js = {
            'root_node': root_node.render(target='js'),
            'test_node_0': test_node_0.render(target='js'),
            'test_node_1': test_node_1.render(target='js')
        }

        self.assert_rendered_html_base_parameters(rendered_html, 'root_node')
        self.assert_rendered_html_base_parameters(rendered_html, 'test_node_0')
        self.assert_rendered_html_base_parameters(rendered_html, 'test_node_1')

        for key, rendered_js in rendered_js.iteritems():
            self.assert_rendered_js_base_parameters(rendered_js)
