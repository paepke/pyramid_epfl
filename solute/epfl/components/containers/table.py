from solute.epfl.core import epflcomponentbase



class TextValue(epflcomponentbase.ComponentBase):
    template_name = "containers/textvalue.html"
    asset_spec = "solute.epfl.components:containers/static"
    value = None
    compo_state = ["value"]


