
from solute.epfl.core import epflcomponentbase

class Headbar(epflcomponentbase.ComponentBase):
    template_name = "headbar/headbar.html"

    compo_state = ['username', 'title','titlelink','usergroup','optionslink']

    title = ""
    username = ""
    titlelink = "#"
    usergroup = ""
    optionslink = "#"