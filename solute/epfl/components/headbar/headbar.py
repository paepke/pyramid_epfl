
from solute.epfl.core import epflcomponentbase

class Headbar(epflcomponentbase.ComponentBase):
    template_name = "headbar/headbar.html"

    compo_state = ['username', 'title','titlelink','usergroup','optionslink']

    title = ""
    title_hover_text = None
    username = ""
    titlelink = "#"
    usergroup = ""
    optionslink = "#"
    logoutlink = "#"
    logout_hover_text = "Logout"

    def handle_logout(self,redirect):
        #Overwrite me for logout handling
        pass