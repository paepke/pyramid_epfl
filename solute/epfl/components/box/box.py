# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Box(epflcomponentbase.ComponentContainerBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    asset_spec = "solute.epfl.components:box/static"
    theme_path = ['box/theme']

    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["box/box.js"]
    css_name = ["box.css"]
    js_name = ["box.js"]

    auto_visibility = True # the visibility of the box depends on the visibility of the containing template-elements
                           # if none of them (compos or form-fields) are visible the box to is not visible
                           # else the box is visible

    compo_config = epflcomponentbase.ComponentContainerBase.compo_config[:]
    compo_config.append("auto_visibility")

    box_shown = True
    is_removable = False
    is_draggable = False
    
    def handle_removed(self):
        self.delete_component()
    
    def after_event_handling(self):
        super(Box, self).after_event_handling()

        # calculate visibility by checking all sub-element's visibility
        if self.auto_visibility:

            if not self.components:
                return True # No subelements -> I am visible!

            some_visible = False
            for el in self.components:
                if el.is_visible():
                    some_visible = True # at least one subelement is visible -> I am visible!
                    break

            # Automatic redraw-handling based on the old visibility state:
            if some_visible:
                old_visibility = self.set_visible()
                if not old_visibility:
                    self.redraw()
            else:
                old_visibility = self.set_hidden()
                if old_visibility:
                    self.redraw()

