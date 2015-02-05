from solute.epfl.core import epflcomponentbase


class Dragable(epflcomponentbase.ComponentContainerBase):
    template_name = "dragable/dragable.html"
    js_parts = epflcomponentbase.ComponentContainerBase.js_parts + ["dragable/dragable.js"]
    asset_spec = "solute.epfl.components:dragable/static"

    css_name = ["dragable.css"]
    js_name = ["dragable.js"]

    compo_config = []
    compo_state = ["id", "title", "is_selected"]

    type = "dragable"
    id = None
    title =None
    title_renamable = False
    is_selected = False
    selectable=False

    @classmethod
    def generate_from_id(cls, id):
        result = cls()
        result.id = id
        return result
    
    def handle_rename_title(self, title):
        self.title = title