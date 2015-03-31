# * encoding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ListLayout, PaginatedListLayout


class ContextListEntry(epflcomponentbase.ComponentContainerBase):

    """
    Only for internal use as child compo of ContextListLayout

    """
    template_name = "context_list_layout/entry.html"
    asset_spec = "solute.epfl.components:context_list_layout/static"


class ContextListLayout(PaginatedListLayout):

    """
    A searchable list layout with a context menu in every row.

    Its content and the context menu is configured using get_data()
    example

    .. code-block:: python

        menu = [{'name':"move up", 'event':"move_up", 'type':"link"},
                {'name':"move down", 'event':"move_down", 'type'"link"},
                {'type':"divider"},
                {'name':u"delete", 'event':"delete", 'type':"link"},
                {'name':"rename", 'event':"rename", 'type':"link"}]

        data = []
        for i in range(0, 100):
            data.append({'id': i, "data": "test" + str(i), 'menu':menu})



    A click on a context menu entry emits an event which have to be handled
    for example the entry

    .. code-block:: python

        {'name':"rename", 'event':"rename", 'type':"link"}

    have to be handled by

    .. code-block:: python

        def handle_rename(self, id, data):
            pass

    """

    theme_path = {'default': ['context_list_layout/theme'],
                  'container': ['pretty_list_layout/theme'],
                  # context layout embraces paginated layout template  for before and after
                  # templates
                  'before': ['pretty_list_layout/theme', '<paginated_list_layout/theme', '<context_list_layout/theme'],
                  'after': ['pretty_list_layout/theme', '<paginated_list_layout/theme', '<context_list_layout/theme']}

    js_parts = PaginatedListLayout.js_parts + ['context_list_layout/context_list_layout.js']
    default_child_cls = ContextListEntry

    show_pagination = False
    show_search = True

    auto_update_children = True

    js_name = PaginatedListLayout.js_name + [("solute.epfl.components:context_list_layout/static", "context_list_layout.js"),
                                             ("solute.epfl.components:context_list_layout/static", "contextmenu.js")]
    css_name = PaginatedListLayout.css_name + [("solute.epfl.components:context_list_layout/static", "context_list_layout.css")]

    data_interface = {'id': None, 'data': None, 'menu': None}