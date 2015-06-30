# * encoding: utf-8

from __future__ import unicode_literals

from solute.epfl.components.form.form import FormInputBase


class ColorThief(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorthief/static", "colorthief.js"),("solute.epfl.components:colorthief/static", "color-thief.min.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorthief/static", "colorthief.css")]
    template_name = "colorthief/colorthief.html"

    new_style_compo = True

    compo_js_params = ['fire_change_immediately']
    compo_js_name = 'ColorThief'
    compo_js_extras = ['handle_click']
