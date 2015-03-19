
from solute.epfl.core import epflcomponentbase

class Headbar(epflcomponentbase.ComponentBase):
    """
    A Headbar component which should always displayed on top.

    """
    template_name = "headbar/headbar.html"
    asset_spec = "solute.epfl.components:headbar/static"

    css_name = ["headbar.css"]

    compo_state = ['username', 'title','titlelink','usergroup','optionslink',"breadcrumb_first","breadcrumb_second"]

    title = None #: The title shown in the left corner
    title_hover_text = None
    username = None #: Username shown next to title
    titlelink = None #: The link when you click on title
    usergroup = None #: The usergroup shown next to username
    logoutlink = None #: Where the logout goes to
    logout_hover_text = "Logout"

    breadcrumb_first = None
    breadcrumb_second = None

    def handle_logout(self,redirect):
        """
        Overwrite me for logout handling

        This is called when you click on logout

        """
        pass