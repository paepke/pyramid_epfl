# * encoding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ListLayout


class ContextListEntry(epflcomponentbase.ComponentContainerBase):
    """
    Only for internal use as child compo of ContextListLayout

    """
    template_name = "context_list_layout/entry.html"
    asset_spec = "solute.epfl.components:context_list_layout/static"


class ContextListLayout(ListLayout):
    """
    A searchable list layout with a context menu in every row

    The context menu is configured over get_data
    example

    .. code-block:: python

        menu = [{"name":"move up","event":"move_up","type":"link"},
                {"name":"move down","event":"move_down","type":"link"},
                {"type":"divider"},
                {"name":u"delete","event":"delete","type":"link"},
                {"name":"rename","event":"rename","type":"link"}]

        data = []
        for i in range(0, 100):
            data.append({"id": i, "data": "test" + str(i),"menu":menu})



    A click on a context menu entry emits an event which have to be handeled
    for example the entry

    .. code-block:: python

        {"name":"rename","event":"rename","type":"link"}

    have to be handled by

    .. code-block:: python

        def handle_delete(self,id,data):
            pass

    """

    asset_spec = "solute.epfl.components:context_list_layout/static"
    theme_path = ['paginated_list_layout/theme', 'context_list_layout/theme']

    js_parts = ListLayout.js_parts[:]
    js_parts.extend(['paginated_list_layout/paginated_list_layout.js', 'context_list_layout/context_list_layout.js'])
    default_child_cls = ContextListEntry

    show_pagination = False
    show_search = True

    auto_update_children = True

    js_name = ["context_list_layout.js"]
    css_name = ["context_list_layout.css"]

    data_interface = {'id': None, 'data': None, 'menu': None}
    height = 400
