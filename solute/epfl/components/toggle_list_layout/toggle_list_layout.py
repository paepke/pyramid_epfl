# coding: utf-8

"""

"""

from solute.epfl.components import PrettyListLayout


class ToggleListLayout(PrettyListLayout):
    theme_path = {'default': ['pretty_list_layout/theme', '<toggle_list_layout/theme'], # toggle layout embraces pretty layout (for default templates)
                  'container': ['pretty_list_layout/theme', '>toggle_list_layout/theme']} # pretty layout embraces toggle layout (for container template only)
    
    js_parts = PrettyListLayout.js_parts + ["toggle_list_layout/toggle_list_layout.js"]

    compo_state = PrettyListLayout.compo_state + ['show_children']

    show_children = True

    def handle_show(self):
        self.show_children = True
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        self.redraw()






