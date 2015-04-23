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

    def __init__(self, page, cid, show_search=True, get_data=None, default_child_cls=None, data_interface=None, *args, **kwargs):
        """ContextListLayout Component

        :param get_data: List of get_data sources. First entry is used for first level, second for second, and so on.
        :param show_search:
        :param default_child_cls: Default component to be used to initialize children.
        :param data_interface: Data interface to translate the results from get_data polling. If a list is given it will
                               be used for the according levels given in the get_data list. Else this is used on all
                               children.
        """
        kwargs.update({
            'show_search': show_search,
            'get_data': get_data,
            'default_child_cls': default_child_cls,
            'data_interface': data_interface
        })
        super(ContextListLayout, self).__init__(page, cid, *args, **kwargs)

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

    default_menu = [{'name':u"Delete", 'event':"delete", 'type':"link"},
                    {'name':"Rename", 'event':"rename", 'type':"link"}]

    def handle_delete(self, entry_id, data):
        pass

    def handle_rename(self, entry_id, data):
        pass
