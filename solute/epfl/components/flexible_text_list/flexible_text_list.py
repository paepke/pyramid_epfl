# coding: utf-8

from solute.epfl.core import epflcomponentbase
from solute.epfl.components import ContextListLayout, ContextListEntry, ColLayout, Form, TextInput, Button


class FlexibleTextList(epflcomponentbase.ComponentContainerBase):
    """
    A container component containing a context_text_list and an add formular

    The list can be configured as searchable and extensible.
    """

    def __init__(self, page, cid, data_interface=None, get_data=None, show_search=False,
                 height=None, show_add_form=False, context_menus=None, *args, **kwargs):
        """FlexibleTextList component

        :param data_interface: Data interface to translate the results from get_data polling.
        :param get_data: A get_data source that is used for this component
        :param show_search: Show or hide a search form on top of the list
        :param height: Set a maximum height to the list
        :param show_add_form: Show or hide a form on the bottom of the list to dynamically add new entries to the list
        :param context_menus: Show a default context-menu if no context-menus are provided by the get_data function
        """
        kwargs.update({
            'data_interface': data_interface,
            'get_data': get_data,
            'show_search': show_search,
            'height': height,
            'show_add_form': show_add_form,
            'context_menus': context_menus
        })
        super(FlexibleTextList, self).__init__(page, cid, *args, **kwargs)


    asset_spec = "solute.epfl.components:flexible_text_list/static"

    template_name = "flexible_text_list/flexible_text_list.html"

    compo_config = epflcomponentbase.ComponentContainerBase.compo_config + \
                   ["show_search", "show_add_form"]

    data_interface = {
        'id': None,
        'data': None,
        'menu': None
    }

    default_child_cls = ContextListEntry

    #: If true, a search bar and search functionality is provided.
    show_search = False

    #: The max height of the list view. If the entries exceed the height, a scrollbar is displayed.
    height = None

    #: If true, an input field and a button will be displayed at the bottom to handle adding new entries.
    show_add_form = False

    #: If true, context menus will be displayed on each item in the list. ContextMenus can be provided by get_data parameter 'menu', if none is provided contect_list_layout contains a default menu.
    context_menus = None

    def init_struct(self):
        self.node_list = [
            ContextListLayout(
                show_search=self.show_search,
                get_data=self.get_data,
                height=self.height,
                data_interface=self.data_interface,
                default_child_cls=self.default_child_cls,
                menu=self.context_menus
            )
        ]
        if self.show_add_form:
            self.node_list.append(
                Form(
                    node_list=[
                        ColLayout(
                            node_list=[
                                TextInput(
                                    placeholder=u'Element hinzufügen',
                                    cols=7
                                ),
                                Button(
                                    value=u"Hinzufügen",
                                    event_name="add_list_entry",
                                    color='default',
                                    cols=5
                                )
                            ]
                        )
                    ]
                )
            )

    def is_smart(self):
        return False

    def handle_add_list_entry(self):
        pass
