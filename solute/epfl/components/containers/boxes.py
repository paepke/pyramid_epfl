# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Box(epflcomponentbase.ComponentTreeBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "containers/box.html"
    asset_spec = "solute.epfl.components:containers/static"

    css_name = ["box.css"]

    auto_visibility = True # the visibility of the box depends on the visibility of the containing template-elements
                           # if none of them (compos or form-fields) are visible the box to is not visible
                           # else the box is visible

    compo_config = ["auto_visibility"]

    box_shown = True
    
    def after_event_handling(self):
        super(Box, self).after_event_handling()

        # calculate visibility by checking all sub-element's visibility
        if self.auto_visibility:

            els = self.get_template_subelements()

            if not els:
                return True # No subelements -> I am visible!

            some_visible = False
            for el in els:
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

