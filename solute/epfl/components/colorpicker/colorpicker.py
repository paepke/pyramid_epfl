# * encoding: utf-8

from __future__ import unicode_literals

from solute.epfl.components.form.form import FormInputBase


class ColorPicker(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorpicker/static", "colorpicker.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorpicker/static", "colorpicker.css")]
    template_name = "colorpicker/colorpicker.html"

    new_style_compo = True

    compo_js_params = ['fire_change_immediately']
    compo_js_name = 'ColorPicker'
    compo_js_extras = ['handle_click']

    TYPE_RGB = 0
    TYPE_SPECIAL = 1

    compo_state = FormInputBase.compo_state + ["value_options"]

    # value = []

    value_options = [
        {"data": "#FF0000", "type": TYPE_RGB, "text": "Rot"},
        {"data": "Silber", "type": TYPE_SPECIAL, },
        {"data": "Bronze", "type": TYPE_SPECIAL, },
        {"data": "Gold", "type": TYPE_SPECIAL, },
        {"data": "#00FF00", "type": TYPE_RGB, },
        {"data": "#0000FF", "type": TYPE_RGB, },
        {"data": "#00FFFF", "type": TYPE_RGB, },
        {"data": "#FFFFFF", "type": TYPE_RGB, },
        {"data": "#000000", "type": TYPE_RGB, },
        {"data": "#FF00FF", "type": TYPE_RGB, "text": "Pink"},
    ]

    def handle_change(self, value):
        if self.value is None:
            self.value = []

        # check if value is in self value if true remove else add
        full_value = [val for val in self.value_options if val["data"] == value][0]
        if full_value in self.value:
            self.value.remove(full_value)
        else:
            self.value.append(full_value)

        self.redraw()