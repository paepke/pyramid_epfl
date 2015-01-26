from solute.epfl.core.epflcomponentbase import ComponentBase


class Sidebar(ComponentBase):
    template_name = "sidebar/sidebar.html"

    asset_spec = "solute.epfl.components:sidebar/static"

    compo_state = ["links"]

    links = []

