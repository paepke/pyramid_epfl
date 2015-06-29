# * encoding: utf-8

from __future__ import unicode_literals

from solute.epfl.components.form.form import FormInputBase


class ColorPicker(FormInputBase):

    js_name = FormInputBase.js_name + [("solute.epfl.components:colorpicker/static","colorpicker.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorpicker/static","colorpicker.css")]
    template_name = "colorpicker/colorpicker.html"


    new_style_compo = True

    compo_js_params = ['fire_change_immediately']
    compo_js_name = 'ColorPicker'