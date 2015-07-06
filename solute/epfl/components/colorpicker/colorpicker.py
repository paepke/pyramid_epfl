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
    compo_state = FormInputBase.compo_state + ["value_options"]
    js_parts = []

    TYPE_RGB = 0  #: Constant for value options list, show data as rgb

    TYPE_SPECIAL = 1  #: Constant for value options list, show data as special

    value_options = []  #: list of available colors in the format {data: #hex,type:TYPE_RGB|TYPE_SPECIAL,optional: text}

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

    def __init__(self, page, cid, value_options=None, **extra_params):
        """
        ColorPicker compo displays a selectable list of colors, or special values such as transparent
        :param value_options: list of available colors in the format {data: #hex,type:TYPE_RGB|TYPE_SPECIAL,optional: text}
        """
        super(ColorPicker, self).__init__(page=page,cid=cid,value_options=value_options,**extra_params)
