# coding: utf-8

"""

"""
from pyramid import security

from solute.epfl.core import epflcomponentbase


class Image(epflcomponentbase.ComponentBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "image/image.html"
    js_parts = []  # epflcomponentbase.ComponentBase.js_parts + ["image/image.js"]
    asset_spec = "solute.epfl.components:image/static"

    css_name = ["image.css"]
    js_name = ["color-thief.min.js", "imagesloaded.pkgd.min.js", "image.js"]

    compo_config = []
    compo_state = ["image_path"]

    image_path = None
    show_dominant_color = False
    show_additional_colors = False
    height = None
    width = None
    padding = False

    new_style_compo = True
    compo_js_name = 'Image'
    compo_js_params = ['show_dominant_color', 'show_additional_colors']
    compo_js_extras = ['handle_drag']

    def get_image_path(self):
        if self.image_path is None:
            self.image_path = ""
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path
