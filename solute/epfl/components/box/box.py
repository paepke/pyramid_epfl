# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil


class Box(epflcomponentbase.ComponentContainerBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    asset_spec = "solute.epfl.components:box/static"
    theme_path = ['box/theme']

    compo_state = epflcomponentbase.ComponentContainerBase.compo_state + ['title']
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["box/box.js"]
    css_name = ["box.css"]
    js_name = ["box.js"]

    # : The title of a box. If it is set, a heading panel is rendered that contains the title.
    title = None

    #: the visibility of the box depends on the visibility of the containing template-elements
    #: if none of them (compos or form-fields) are visible the box to is not visible
    #: else the box is visible
    auto_visibility = True

    #: Set to true if box should not be displayed inside its parent component, but rendered as modal hover box on the overall page.
    hover_box = False
    #: Indicates whether a hover box component should be deleted upon close or just be hidden.
    hover_box_remove_on_close = True
    #: Indicates of a border should be drawn around the box.
    box_shown = True
    #: Indicates if the title of the box should be shown. Sometimes, you want to specify a title but not show it inside the box.
    #: For example, a box inside a :class:`solute.epfl.components.tabs_layout.tabs_layout.TabsLayout` component.
    show_title = True
    #: Indicates whether a box can be closed by clicking on a special 'close' button
    is_removable = False

    def handle_removed(self):
        self.delete_component()

    def handle_hide(self):
        self.set_hidden()

    def after_event_handling(self):
        super(Box, self).after_event_handling()

        # calculate visibility by checking all sub-element's visibility
        if self.auto_visibility:

            if not self.components:
                return True  # No subelements -> I am visible!

            some_visible = False
            for el in self.components:
                if el.is_visible(check_parents=False):
                    some_visible = True  # at least one subelement is visible -> I am visible!
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


class ModalBox(Box):
    hover_box = True  #: see :attr:`Box.hover_box`
    visible = False  #: see :attr:`Box.hover_box`
    auto_visibility = False  #: see :attr:`Box.hover_box`
    is_removable = True  #: see :attr:`Box.hover_box`
    hover_box_remove_on_close = False  #: see :attr:`Box.hover_box`
    #: Used to specify the width of the modal. The width is given in percentage of the full page width.
    hover_box_width = 50

    def open(self):
        """
        Open and display the modal box.
        """
        self.set_visible()
        self.redraw()
        self.add_ajax_response("$('body').css({ overflow: 'hidden' });")

    def handle_hide(self):
        """
        Called when modal box is closed.
        """
        Box.handle_hide(self)
        self.redraw()
        self.add_ajax_response("$('body').css({ overflow: 'inherit' });")
