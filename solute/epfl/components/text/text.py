from solute.epfl.core import epflcomponentbase


class Text(epflcomponentbase.ComponentBase):
    template_name = "text/text.html"
    value = None
    verbose = False
    tag = None
    tag_class = None
    #: If set, display a label before the text. In this case, the :attr:`verbose` attribute is not needed and
    # will be neglected, since verbose tags will be rendered anyway.
    label = None
    #: If set to True, the label will be rendered above the text instead of left before the text.
    # This attribute is only regarded if the :attr:`label` attribute is set.
    layout_vertical = False
    compo_state = epflcomponentbase.ComponentBase.compo_state + ["value", "tag", "tag_class", "verbose", "label"]

    def __init__(self, value=None, verbose=False, tag=None, tag_class=False, label=None, vertical_layout=False, **extra_params):
        super(Text, self).__init__()
