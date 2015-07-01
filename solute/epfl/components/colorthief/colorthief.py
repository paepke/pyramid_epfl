# * encoding: utf-8

from __future__ import unicode_literals

from solute.epfl.components.form.form import FormInputBase


class ColorThief(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorthief/static", "colorthief.js"),
                                       ("solute.epfl.components:colorthief/static", "color-thief.min.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorthief/static", "colorthief.css")]
    template_name = "colorthief/colorthief.html"

    new_style_compo = True

    compo_js_params = ['fire_change_immediately','colors_count']
    compo_js_name = 'ColorThief'
    compo_js_extras = ['handle_click']

    compo_state = FormInputBase.compo_state + ["drop_zone_height","image_src","dominat_colors_count"]

    drop_zone_height = 150

    image_src = None

    colors_count = 8

    def handle_change(self, value, image_src=None):
        self.value = ["rgb(%d,%d,%d)" % (val[0], val[1], val[2]) for val in value]
        self.image_src = image_src

        print value, image_src
        self.redraw()
