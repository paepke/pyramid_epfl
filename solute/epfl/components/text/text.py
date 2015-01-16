from solute.epfl.core import epflcomponentbase



class Text(epflcomponentbase.ComponentBase):
    template_name = "text/text.html"
    value = None
    compo_state = ["value"]


