
from solute.epfl.core import epflcomponentbase

class Headbar(epflcomponentbase.ComponentBase):
    """
    A Headbar component which should always displayed on top.

    """
    template_name = "headbar/headbar.html"
    asset_spec = "solute.epfl.components:headbar/static"

    css_name = ["headbar.css"]

    compo_state = ['username', 'title','titlelink','usergroup','optionslink']

    title = "" #: The title shown in the left corner
    title_hover_text = None
    username = "" #: Username shown next to title
    titlelink = "#" #: The link when you click on title
    usergroup = "" #: The usergroup shown next to username
    optionslink = "#"
    logoutlink = "#" #: Where the logout goes to
    logout_hover_text = "Logout"

    def handle_logout(self,redirect):
        """
        Overwrite me for logout handling

        This is called when you click on logout

        """
        pass