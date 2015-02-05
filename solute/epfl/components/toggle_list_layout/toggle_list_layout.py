# coding: utf-8

"""

"""

from solute.epfl.components import PrettyListLayout


class ToggleListLayout(PrettyListLayout):
    theme_path = {'default': ['pretty_list_layout/theme', '<toggle_list_layout/theme'],
                  'container': ['pretty_list_layout/theme', '>toggle_list_layout/theme']}
    
    js_parts = PrettyListLayout.js_parts + ["toggle_list_layout/toggle_list_layout.js"]

    compo_state = PrettyListLayout.compo_state + ['show_children']

    show_children = True

    def handle_show(self):
        self.show_children = True
        self.redraw()

    def handle_hide(self):
        self.show_children = False
        self.redraw()






