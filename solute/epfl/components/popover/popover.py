from solute.epfl.core import epflcomponentbase

class Popover(epflcomponentbase.ComponentBase):
    """
    Popover dialog (a click triggered tooltip) using bootstrap popover

    Example: http://getbootstrap.com/javascript/#popovers

    """

    template_name = "popover/popover.html"

    js_parts = epflcomponentbase.ComponentBase.js_parts + ["popover/popover.js"]
    asset_spec = "solute.epfl.components:popover/static"

    js_name = ["popover.js"]

    compo_config = []
    compo_state = ["text", "title","position"]

    text = []
    title = None #: if title is none it is not displayed
    position = "top" #: posible positions are top,left,right,bottom
