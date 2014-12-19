from solute.epfl.core import epflcomponentbase


class Dragable(epflcomponentbase.ComponentTreeBase):
    template_name = "dragable/dragable.html"
    asset_spec = "solute.epfl.components:dragable/static"

    css_name = ["dragable.css"]
    js_name = ["dragable.js"]

    compo_config = []
    compo_state = ["id"]

    type = "dragable"
    id = None

    @classmethod
    def generate_from_id(cls, id):
        result = cls()
        result.id = id
        return result