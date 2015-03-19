# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.components import Box


class DragBox(Box):

    js_parts = Box.js_parts + ["drag_box/drag_box.js"]
    js_name = Box.js_name + [("solute.epfl.components:drag_box/static", "drag_box.js"), "drag.js"]

    compo_state = Box.compo_state + ["disable_drag", "keep_orig_in_place"]
    #: If set to true, this component renders as a normal box and with disabled draggability. Useful for on-the-fly draggability toggling.
    disable_drag = None
    #: If set to true, the dragged element is cloned and the original element is kept in place.
    keep_orig_in_place = None
