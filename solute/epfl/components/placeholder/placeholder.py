from solute.epfl.core import epflcomponentbase


class Placeholder(epflcomponentbase.ComponentBase):
    template_name = "placeholder/placeholder.html"
    type = None  #: Type of the placeholder, can be set to "hr" else defaults to br tag.

    def __init__(self, page, cid, type=None, **extra_params):
        super(Placeholder, self).__init__(page, cid, type=type, **extra_params)
