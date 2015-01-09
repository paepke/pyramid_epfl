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
        for theme_path in reversed(self.theme_path):
            try:
                return env.get_template('%s/%s' % (theme_path, target))
            except TemplateNotFound:
                continue
        return env.get_template('%s/%s' % (self.theme_path_default, target))

    def get_render_environment(self, env):
        result = {'compo': self}
        result.update({'container': self.get_themed_template(env, 'container.html').module.render,
                       'row': self.get_themed_template(env, 'row.html').module.render,
                       'before': self.get_themed_template(env, 'before.html').module.render,
                       'after': self.get_themed_template(env, 'after.html').module.render})
        return result


class PrettyListLayout(ListLayout):
    template_prefix = ListLayout.template_prefix
    theme_path = ['layout/list/pretty']


class PaginatedListLayout(PrettyListLayout):
    theme_path = ['layout/list/pretty', 'layout/list/paginated']
    js_parts = ['layout/list/paginated.js']
