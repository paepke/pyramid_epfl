from solute.epfl.core import epflcomponentbase


class RecursiveTree(epflcomponentbase.ComponentContainerBase):
    asset_spec = 'solute.epfl.components:recursive_tree/static'

    theme_path = ['recursive_tree/theme']

    js_name = ['recursive_tree.js']

    css_name = ['recursive_tree.css']

    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + [
        'icon_open', 'icon_close', 'label', 'get_data', 'show_children', 'data_interface','scroll_position'
    ]
    icon_open = None
    icon_close = None
    label = None

    id = None

    data_interface = {'id': None, 'label': None, 'icon_open': None, 'icon_close': None}

    show_children = False

    scroll_position = None

    new_style_compo = True
    compo_js_params = ['scroll_position']
    compo_js_extras = []
    compo_js_name = 'RecursiveTree'

    def __init__(self, page, cid, show_children=False, get_data=None, default_child_cls=None, data_interface=None,
                 *args, **kwargs):
        """Simple tree component.

        :param show_children: Load and show any potential children that would be returned by polling get_data.
        :param get_data: List of get_data sources. First entry is used for first level, second for second, and so on.
        :param default_child_cls: Default component to be used to initialize children.
        :param data_interface: Data interface to translate the results from get_data polling. If a list is given it will
                               be used for the according levels given in the get_data list. Else this is used on all
                               children.
        """
        super(RecursiveTree, self).__init__(page, cid, show_children, get_data, default_child_cls, *args, **kwargs)

    def init_struct(self):
        if self.default_child_cls is None:
            self.default_child_cls = RecursiveTree(data_interface=self.data_interface)
        if type(self.get_data) is list:
            data = self.get_data[:]
            self.get_data = data.pop(0)
            if len(data) > 0:
                if type(self.data_interface) is list:
                    data_interface = self.data_interface[:]
                    self.data_interface = data_interface.pop(0)
                    self.default_child_cls = self.default_child_cls(get_data=data, data_interface=data_interface)
                else:
                    self.default_child_cls = self.default_child_cls(get_data=data)

    def handle_click_label(self):
        pass

    def handle_click_icon(self):
        self.show_children = not self.show_children

    def _get_data(self, *args, **kwargs):
        if self.show_children:
            return super(RecursiveTree, self)._get_data(*args, **kwargs)
        return []

    def handle_scroll(self,scroll_pos):
        self.scroll_position = scroll_pos
