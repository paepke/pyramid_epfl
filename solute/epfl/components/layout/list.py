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
    show_pagination = True
    show_search = True

    theme_path = ['layout/list/pretty', 'layout/list/paginated']
    js_parts = ['layout/list/paginated.js']


class LinkListLayout(PaginatedListLayout):
    default_child_cls = epflcomponentbase.ComponentBase
    data_interface = {'id': None,
                      'text': None,
                      'url': None}
    theme_path = ['layout/list/pretty', 'layout/list/paginated', 'layout/list/link']
    js_parts = ['layout/list/paginated.js', 'layout/list/link_list.js']

    compo_state = PrettyListLayout.compo_state[:]
    compo_state.extend(['links'])

    def get_data(self, row_offset=None, row_limit=None, row_data=None):
        for i, link in enumerate(self.links):
            link['id'] = i
        return self.links


class HoverLinkListLayout(LinkListLayout):
    data_interface = {'id': None,
                      'text': None,
                      'src': None,
                      'url': None}
    js_parts = ['layout/list/paginated.js', 'layout/list/link_list.js', 'layout/list/hover.js']



