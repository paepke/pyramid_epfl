from solute import epfl
import os
import inspect
import re


def assert_style(component):
    __tracebackhide__ = True

    compo_name = component.__name__

    errors = []

    errors += assert_style_structure(component, compo_name)

    init_func = component.__init__
    init_docs = init_func.__doc__
    init_code = init_func.func_code

    errors += assert_style_init(component, compo_name, init_func, init_code, init_docs)

    errors += assert_style_docs(component)

    assert len(errors) == 0, "\n" + "\n".join(errors)


def assert_style_structure(component, compo_name):
    __tracebackhide__ = True

    errors = []

    if getattr(component, 'asset_spec', None) is None \
            or ':{compo_name}/'.format(compo_name=compo_name.lower()) not in component.asset_spec:
        return errors

    file_path = inspect.getsourcefile(component)
    file_path = os.path.abspath(file_path)
    js_file_path = file_path[:-3] + '.js'

    package_path = os.path.dirname(file_path)

    static_path = package_path + '/static'
    static_js_file_path = static_path + '/{compo_name}.js'.format(compo_name=compo_name.lower())

    if not file_path.endswith(compo_name.lower() + '.py'):
        errors.append("{compo_name} is missing primary python file.".format(compo_name=compo_name))
    if not package_path.endswith(compo_name.lower()):
        errors.append(
            "{compo_name} has a malformed package path. Should end with {compo_name_lower} actually is {package_path}."
            .format(
                compo_name=compo_name,
                compo_name_lower=compo_name.lower(),
                package_path=package_path,
            ))
    assert os.path.exists(static_path), "{compo_name} is missing static folder.".format(
        compo_name=compo_name)

    if os.path.exists(js_file_path):
        js_file = file(js_file_path).read()
        assert js_file.startswith('epfl.init_component("{{ compo.cid }}"'), \
            '{compo_name} has dynamic js missing \'epfl.init_component("{{{{ compo.cid }}}}"\''.format(
                compo_name=compo_name)
        assert js_file.startswith('epfl.init_component("{{ compo.cid }}", "%s", {' % compo_name), \
            '{compo_name} has dynamic js missing ' \
            '\'epfl.init_component("{{{{ compo.cid }}}}", "{compo_name}"\''.format(
                compo_name=compo_name)
    if os.path.exists(static_js_file_path):
        js_file = file(static_js_file_path).read()

        r = re.compile("epfl\.{compo_name}\.inherits_from\(epfl\.([A-Za-z]*)\);".format(
            compo_name=compo_name))
        result = r.findall(js_file)
        assert len(result) == 1, \
            "{compo_name} is missing inheritance calls in static js.".format(compo_name=compo_name)
        assert js_file.count("epfl.{base_compo}.call(this, cid, params);".format(base_compo=result[0])) == 1, \
            "{compo_name} is missing inherited initiation call in static js. " \
            "'epfl.{base_compo}.call(this, cid, params);' not found".format(
                compo_name=compo_name, base_compo=result[0])

        assert js_file.startswith("epfl.{compo_name} = function(cid, params) ".format(
            compo_name=compo_name)), \
            "{compo_name} is not correctly created in static js."
        assert js_file.count("epfl.{compo_name}.inherits_from(epfl.".format(
            compo_name=compo_name)) == 1, \
            "{compo_name} is not correctly inheriting in static js."

    return []


def assert_style_init(component, compo_name, init_func, init_code, init_docs):
    __tracebackhide__ = True
    errors = []
    if component in [epfl.core.epflcomponentbase.ComponentBase,
                     epfl.core.epflcomponentbase.ComponentContainerBase]:
        # Both bases are exempt from these requirements, since they do not have an API to be exposed in this fashion.
        return errors

    if not init_docs:
        errors.append("{compo_name} __init__ method has no doc string.".format(compo_name=compo_name))
        return errors

    if 'page' not in init_code.co_varnames:
        errors.append(
            "{compo_name} __init__ method is not correctly setup. (Missing page parameter, or not overwritten.)"
            .format(compo_name=compo_name)
        )

    for position, name in [(0, 'self'), (1, 'page'), (2, 'cid'), (-1, ('extra_params', 'kwargs'))]:
        if init_code.co_varnames[position] == name:
            continue
        if type(name) is tuple:
            if init_code.co_varnames[position] in name:
                continue
            name = "' or '".join(name)

        errors.append("{compo_name} __init__ method is missing or misplacing parameter '{name}'.".format(
            compo_name=compo_name,
            name=name
        ))

    for var in init_code.co_varnames:
        if var in ['self', 'page', 'args', 'kwargs', 'extra_params', 'cid']:
            continue
        if ":param {var}:".format(var=var) not in init_docs:
            errors.append(
                "{compo_name} __init__ method is missing docs for {param}.".format(compo_name=compo_name, param=var)
            )

    return errors


def assert_style_docs(component):
    __tracebackhide__ = True
    errors = []

    source, starting_line = inspect.getsourcelines(component)

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

        if attr_name in ['cid', 'slot']:
            errors.append(
                "Invalid attribute set: 'slot' and 'cid' are reserved names. (Line: {line_number})"
                .format(line_number=abs_line_number))
            continue

        attr_tail = search_result[0].strip().split(' ', 2)[2]
        if '#' in attr_tail:
            if '  #: ' not in attr_tail:
                errors.append(
                    "Bad format on docstring for {attr_name}. Expected string containing '  #: ', got '{attr_tail}'"
                    " instead. (Line: {line_number})"
                    .format(attr_name=attr_name, attr_tail=attr_tail, line_number=abs_line_number))
            continue

        line_cursor = 1
        current_line = source[line_number - line_cursor]
        # No doc string yet, so look backwards.
        if not doc_line.match(current_line):
            errors.append(
                "No docstring found for {attr_name}. Expected a line starting with '#: ', got '{current_line}'"
                " instead. (Line: {line_number})"
                .format(
                    attr_name=attr_name, current_line=current_line.strip(), line_number=abs_line_number - line_cursor))

        while current_line.strip().startswith('#') and line_cursor <= current_line:
            if not doc_line.match(current_line):
                errors.append(
                    "Bad format docstring found for {attr_name}. Expected a line starting with '#: ', got "
                    "'{current_line}' instead. (Line: {line_number})"
                    .format(
                        attr_name=attr_name,
                        current_line=current_line.strip(),
                        line_number=abs_line_number - line_cursor
                    )
                )
                break
            current_line = source[line_number - line_cursor]
            line_cursor += 1

    return errors


def assert_rendering(compo_info, html, js):
    """Contains the following checks:
     * An element with the appropriate epflid exists in the generated html.
    """
    __tracebackhide__ = True
    cid = compo_info['cid']

    # TODO: Create appropriate checks for the generated javascript.
    assert html.count(' epflid="{cid}"'.format(cid=cid)) == 1, \
        'The element with the cid "{cid}" is missing in the generated HTML:\n{html}'.format(cid=cid, html=html)


def assert_coherence(component, compo_info):
    """Contains the following checks:
     * Coherence of object instance attributes to transaction compo_info.
     * Coherence of object instance compo_info to transaction compo_info.
     * Coherence and writeability of object instance compo_state attributes into/to transaction compo_info.
    """
    __tracebackhide__ = True

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
