from solute.epfl.core import epflcomponentbase


class Popover(epflcomponentbase.ComponentBase):

    """
    Popover dialog (a click triggered tooltip) using bootstrap popover.
    The popover dialog is displayed when clicking a button.

    Example: http://getbootstrap.com/javascript/#popovers

    """

    template_name = "popover/popover.html"

    js_parts = epflcomponentbase.ComponentBase.js_parts + ["popover/popover.js"]
    asset_spec = "solute.epfl.components:popover/static"

    css_name = ["popover.css"]
    js_name = ["popover.js"]

    compo_config = []
    compo_state = ["text", "title", "position", "label", "icon"]

    text = []
    title = None  # : if title is none it is not displayed
    position = "top"  # : posible positions are top,left,right,bottom
    #: An optional font-awesome icon that should be displayed on the button.
    # Either the :attr:`icon` or the :attr:`label` have to be defined in order to yield a reasonable button.
    icon = None
    #: An optional label that should be displayed on the button.
    # Either the :attr:`icon` or the :attr:`label` have to be defined in order to yield a reasonable button.
    label = None
    
    #def delete_component(self):
    #    self.add_js_response('epfl.destroy_component("{cid}");'.format(cid=self.cid))
    #    epflcomponentbase.ComponentBase.delete_component(self)
        
