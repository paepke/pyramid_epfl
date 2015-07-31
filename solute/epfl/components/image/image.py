# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
from solute.epfl.components import Droppable
import json


class Image(epflcomponentbase.ComponentBase):
    template_name = "image/image.html"
    js_parts = []  # epflcomponentbase.ComponentBase.js_parts + ["image/image.js"]
    asset_spec = "solute.epfl.components:image/static"

    css_name = ["image.css"]
    js_name = ["color-thief.min.js", "imagesloaded.pkgd.min.js", "image.js"]

    compo_state = ["image_path"]

    image_path = None  #: Path to be used as the source of the image.
    show_dominant_color = False  #: Show the color dominant in the picture.
    show_additional_colors = False  #: Show additional prevalent colors in the picture.
    height = None  #: Set a fixed height. This is used directly in css so use "120px" or "10em", etc.
    width = None  #: Set a fixed width. This is used directly in css so use "120px" or "10em", etc.
    padding = False  #: Set a padding. This is used directly in css so use "120px" or "10em", etc.

    new_style_compo = True
    compo_js_name = 'Image'
    compo_js_params = ['show_dominant_color', 'show_additional_colors']
    compo_js_extras = ['handle_drag']

    def __init__(self, page, cid, image_path=None, height=None, width=None, padding=None, **extra_params):
        """Displays an Image.

        :param image_path: Path to be used as the source of the image.
        :param height: Set a fixed height. This is used directly in css so use "120px" or "10em", etc.
        :param width: Set a fixed width. This is used directly in css so use "120px" or "10em", etc.
        :param padding: Set a padding. This is used directly in css so use "120px" or "10em", etc.
        """
        super(Image, self).__init__(page, cid, **extra_params)

    def get_image_path(self):
        if self.image_path is None:
            self.image_path = ""
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path


class ImageList(Droppable):
    template_name = "image/image_list.html"
    
    js_parts = Droppable.js_parts + ["image/image_list.js"]

    show_borders=False
    
    def handle_add_dragable(self, cid, position):
        """
        Insert a copy of the dragable image in the image list and leave the original dragable as is 
        """
        origin_comp = self.page.components[cid].components[0]
        origin_comp_box = self.page.components[cid].container_compo
        
        new_image = self.add_component(Image())
        new_image.image_path = origin_comp.image_path
        origin_comp_box.redraw()
        self.redraw()

    def __init__(self, page, cid, *args, **extra_params):
        super(ImageList, self).__init__(*args, **extra_params)
        if "show_borders" in extra_params:
            self.show_borders = extra_params["show_borders"]
        else:
            self.show_borders = False