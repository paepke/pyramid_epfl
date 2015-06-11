# coding: utf-8
from solute.epfl.components.form.form import FormInputBase


class PlainHtml(FormInputBase):
    asset_spec = "solute.epfl.components:plain_html/static"
    template_name = "plain_html/plain_html.html"
    js_name = ["plain_html.js"]

    compo_state = ["html"]

    html = ''  #: The HTML this component displays
    new_style_compo = True
    compo_js_name = 'PlainHtml'

    def __init__(self, page, cid, html='', **extra_params):
        """ Simple component to display plain html

        Useage:
        .. code-block:: python

            PlainHtml(
                html=u'<h1>Some nice heading</h1><span>With a span</span>'
            )

        :param html: The html this component will display
        """
        super(PlainHtml, self).__init__(page, cid, html=html, **extra_params)
