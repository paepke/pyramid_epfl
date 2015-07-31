# coding: utf-8
from solute.epfl.components.form.inputbase import FormInputBase


class PlainHtml(FormInputBase):
    template_name = "plain_html/plain_html.html"
    js_name = [("solute.epfl.components:plain_html/static", "plain_html.js")]
    js_parts = []

    compo_state = ["value"]
    value = ''  #: The HTML this component displays
    new_style_compo = True
    compo_js_name = 'PlainHtml'
    validation_type = 'text'

    def __init__(self, page, cid, value='', **extra_params):
        """ Simple component to display plain html

        Useage:
        .. code-block:: python

            PlainHtml(
                value=u'<h1>Some nice heading</h1><span>With a span</span>'
            )

        :param value: The html this component will display
        """
        super(PlainHtml, self).__init__(page, cid, value=value, **extra_params)
