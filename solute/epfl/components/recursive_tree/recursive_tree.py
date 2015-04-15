from solute.epfl.core import epflcomponentbase


class RecursiveTree(epflcomponentbase.ComponentContainerBase):
    asset_spec = 'solute.epfl.components:recursive_tree/static'

    theme_path = ['recursive_tree/theme']

    js_parts = ['recursive_tree/recursive_tree.js']
    js_name = ['recursive_tree.js']

    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + [
        'icon_open', 'icon_close', 'label', 'default_child_cls', 'get_data', 'show_children'
    ]
    icon_open = None
    icon_close = None
    label = None

    id = None

    data_interface = {'id': None, 'label': None, 'icon_open': None, 'icon_close': None}

    show_children = False

    def init_struct(self):
        if self.default_child_cls is None:
            self.default_child_cls = RecursiveTree
        if type(self.get_data) is list:
            data = self.get_data[:]
            self.get_data = data.pop(0)
            if len(data) > 0:
                self.default_child_cls = self.default_child_cls(get_data=data)

    def handle_click_label(self):
        pass

    def handle_click_icon(self):
        self.show_children = not self.show_children

    def _get_data(self, *args, **kwargs):
        if self.show_children:
            return super(RecursiveTree, self)._get_data(*args, **kwargs)
        return []
