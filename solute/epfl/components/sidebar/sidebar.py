from solute.epfl.core.epflcomponentbase import ComponentBase
from urlparse import urlparse

class Sidebar(ComponentBase):
    """
    A Component for showing a sidebar

    provide the links in links in a format like this

    .. code-block:: python

        links = [{'name': 'A link collection', 'url': '#', 'icon': 'cogs',
                  "children": [{"name": "Users", "url": "/users"},
                                 {"name": "History", "url": "/history"}]},
                 {'name': 'Another link collection', 'url': '#', 'icon': 'tachometer',
                    "children": [{"name": "child link 1", "url": "/linkone"},
                                 {"name": "child link 2", "url": "/link2"}]}]


    """
    template_name = "sidebar/sidebar.html"

    asset_spec = "solute.epfl.components:sidebar/static"

    css_name = ["sidebar.css"]

    compo_state = ComponentBase.compo_state[:]
    compo_state.extend(["links","current_url"])

    links = []
    current_url = ""

    def setup_component(self):
        self.current_url = urlparse(self.page.request.current_route_url()).path


