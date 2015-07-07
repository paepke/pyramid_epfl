# * encoding: utf-8

from solute.epfl.components.form.form import FormInputBase


class ColorThief(FormInputBase):
    js_name = FormInputBase.js_name + [("solute.epfl.components:colorthief/static", "colorthief.js"),
                                       ("solute.epfl.components:colorthief/static", "color-thief.min.js")]
    css_name = FormInputBase.css_name + [("solute.epfl.components:colorthief/static", "colorthief.css")]
    template_name = "colorthief/colorthief.html"
    new_style_compo = True
    compo_js_params = ['fire_change_immediately', 'color_count']
    compo_js_name = 'ColorThief'
    compo_js_extras = ['handle_click', 'handle_drop']
    js_parts = []

    compo_state = FormInputBase.compo_state + ["drop_zone_height", "image_src", "dominat_colors_count"]

    height = None  #: Compo height in px if none nothing is set

    width = None  #: Compo width in px if none nothing is set

    image_src = None  #: image src if set the drop zone is hidden

    color_count = 8  #: Count of colors which got extracted from the image

    def handle_change(self, value, image_src=None):
        self.value = [{"rgb": "#%x%x%x" % (val[0], val[1], val[2]), "selected": False} for val in
                      value] if value else None
        self.image_src = image_src
        self.redraw()

    def handle_drop_accepts(self, cid, moved_cid):
        self.add_ajax_response('true')

    def handle_click_color(self, color):
        for val in self.value:
            if val["rgb"] == color:
                val["selected"] = not val["selected"]
                break

        self.redraw()

    def __init__(self, page, cid, height=None, width=None, image_src=None, color_count=None, **extra_params):
        """ColorThief Compo: A Drop Area where images can be dropped and their colors get extracted

        :param height: Compo height in px if none nothing is set
        :param width: Compo width in px if none nothing is set
        :param image_src: image src if set the drop zone is hidden
        :param color_count: Count of colors which got extracted from the image
        :return:
        """
        super(ColorThief, self).__init__(page=page, cid=cid, height=height, width=width, image_src=image_src,
                                         color_count=color_count, **extra_params)
