# coding: utf-8

"""

"""

import types
import copy

from pyramid import security

from solute.epfl.core import epflcomponentbase
from solute.epfl.core import epflutil
import json


class Image(epflcomponentbase.ComponentBase):

    __acl__ = [(security.Allow, security.Everyone, 'access')]

    template_name = "image/image.html"
    asset_spec = "solute.epfl.components:image/static"

    js_name = ["color-thief.min.js", "imagesloaded.pkgd.min.js", "image.js"]

    compo_config = []
    compo_state = ["image_path"]

    image_path = ""
    show_dominant_color = False
    show_additional_colors = False

    def get_image_path(self):
        return self.image_path

    def set_image_path(self, path):
        self.image_path = path

    def __init__(self, **extra_params):
        super(Image, self).__init__()
        self.image_path = ""
