from solute.epfl.core import epflcomponentbase


class Placeholder(epflcomponentbase.ComponentBase):
    template_name = "placeholder/placeholder.html"
    type = None
    compo_state = ["type"]


