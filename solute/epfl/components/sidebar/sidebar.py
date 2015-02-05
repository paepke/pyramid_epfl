from solute.epfl.core.epflcomponentbase import ComponentBase
from urlparse import urlparse

class Sidebar(ComponentBase):
    template_name = "sidebar/sidebar.html"

    asset_spec = "solute.epfl.components:sidebar/static"

    css_name = ["sidebar.css"]

    compo_state = ComponentBase.compo_state[:]
    compo_state.extend(["links","current_url"])

    links = []
    current_url = ""

    def setup_component(self):
        self.current_url = urlparse(self.page.request.current_route_url()).path


