from solute.epfl.core import epflcomponentbase


class Text(epflcomponentbase.ComponentBase):
    template_name = "text/text.html"
    value = None
    verbose = False
    tag = None
    tag_class = None
    compo_state = ["value", "tag", "tag_class", "verbose"]


