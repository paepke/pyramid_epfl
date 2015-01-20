# coding: utf-8

"""

"""

import types, copy

from pyramid import security

from solute.epfl.components import Box


class DragBox(Box):

    js_parts = Box.js_parts + ["drag_box/drag_box.js"]
    js_name = Box.js_name + [("solute.epfl.components:drag_box/static", "drag_box.js"), "drag.js"]
    