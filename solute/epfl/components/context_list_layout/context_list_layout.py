# * encoding: utf-8
from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ListLayout


class ContextListEntry(epflcomponentbase.ComponentContainerBase):
    """
    Only for internal use as child compo of TableListLayout

    """
    template_name = "context_list_layout/entry.html"
    asset_spec = "solute.epfl.components:context_list_layout/static"



class ContextListLayout(ListLayout):

    theme_path = ['paginated_list_layout/theme', 'context_list_layout/theme']

    js_parts = ListLayout.js_parts[:]
    js_parts.extend(['paginated_list_layout/paginated_list_layout.js', 'context_list_layout/context_list_layout.js'])
    default_child_cls = ContextListEntry

    show_pagination = False
    show_search = True

    #: False - You have to call update_children yourself, True - epfl call update_children automatically
    auto_update_children = False

   # compo_state = ListLayout.compo_state[:]
    #compo_state.extend(["orderby", "ordertype", "search", "height"])

    js_name = ["context_list_layout.js"]
    asset_spec = "solute.epfl.components:context_list_layout/static"

    data_interface = {'id': None, 'data': None}
    height = 400