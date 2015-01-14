# coding: utf-8

"""

"""

from solute.epfl.core import epflcomponentbase
from jinja2.exceptions import TemplateNotFound


class ListLayout(epflcomponentbase.ComponentContainerBase):
    template_prefix = 'layout/list/'
    template_name = template_prefix + "list.html"

    theme_path_default = 'layout/list/default'
    theme_path = []

    asset_spec = "solute.epfl.components:layout/static"

    css_name = ["bootstrap.min.css"]

    compo_state = epflcomponentbase.ComponentContainerBase.compo_state[:]
    compo_state.append('links')

    links = []

    def __init__(self, node_list=[], links=[], **extra_params):
        super(ListLayout, self).__init__()

    def get_themed_template(self, env, target):
        theme_paths = self.theme_path
        if type(theme_paths) is dict:
            theme_paths = theme_paths.get(target, theme_paths['default'])
        render_funcs = []
        direction = '<'
        for theme_path in reversed(theme_paths):
            try:
                if theme_path[0] in ['<', '>']:
                    direction = theme_path[0]
                    render_funcs.insert(0, env.get_template('%s/%s.html' % (theme_path[1:], target)).module.render)
                    continue
                render_funcs.append(env.get_template('%s/%s.html' % (theme_path, target)).module.render)
                # print 'success', target, render_funcs
                return direction, render_funcs
            except TemplateNotFound:
                continue

        render_funcs.append(env.get_template('%s/%s.html' % (self.theme_path_default, target)).module.render)
        # print 'default', target, render_funcs
        return direction, render_funcs

    def get_render_environment(self, env):
        result = {}

        def wrap(cb, parent=None):
            if type(cb) is tuple:
                direction, cb = cb
                if len(cb) == 1:
                    return wrap(cb[0])
                if direction == '<':
                    return wrap(cb[-1], parent=wrap((direction, cb[:-1])))
                return wrap(cb[0], parent=wrap((direction, cb[1:])))

            def _cb(*args, **kwargs):
                extra_kwargs = result.copy()
                extra_kwargs.update(kwargs)
                out = cb(*args, **extra_kwargs)
                if parent is not None:
                    extra_kwargs['caller'] = lambda: out
                    out = parent(*args, **extra_kwargs)
                return out
            return _cb

        result.update({'compo': self,
                       'container': wrap(self.get_themed_template(env, 'container')),
                       'row': wrap(self.get_themed_template(env, 'row')),
                       'before': wrap(self.get_themed_template(env, 'before')),
                       'after': wrap(self.get_themed_template(env, 'after'))})
        return result


class PrettyListLayout(ListLayout):
    theme_path = ['layout/list/pretty']


class ToggleListLayout(PrettyListLayout):
    theme_path = {'default': ['layout/list/pretty', '<layout/list/toggle'],
                  'container': ['layout/list/pretty', '>layout/list/toggle']}
    js_parts = ['layout/list/toggle.js']

    compo_state = PrettyListLayout.compo_state[:]
    compo_state.extend(['show_children'])

    show_children = True

    def handle_show(self):
        self.show_children = True
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        self.redraw()


class PaginatedListLayout(PrettyListLayout):
    theme_path = ['layout/list/pretty', 'layout/list/paginated']
    js_parts = ['layout/list/paginated.js']


class LinkListLayout(PrettyListLayout):
    data_interface = {'id': None,
                      'text': None,
                      'url': None}
    theme_path = ['layout/list/pretty', 'layout/list/paginated', 'layout/list/link']
    js_parts = ['layout/list/paginated.js', 'layout/list/link_list.js']


class HoverLinkListLayout(LinkListLayout):
    data_interface = {'id': None,
                      'text': None,
                      'src': None,
                      'url': None}
    js_parts = ['layout/list/paginated.js', 'layout/list/link_list.js', 'layout/list/hover.js']



