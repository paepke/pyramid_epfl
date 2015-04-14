from solute.epfl.core import epflcomponentbase


class PopoverContainer(epflcomponentbase.ComponentContainerBase):

    """
    Popover dialog (a click triggered tooltip) using bootstrap popover.
    The popover dialog is displayed when clicking a button.

    Elements in node_list of PopoverContainer get displayed in Popover Dialog

    Example: http://getbootstrap.com/javascript/#popovers

    """

    template_name = "popover_container/popover_container.html"

    js_parts = epflcomponentbase.ComponentBase.js_parts + ["popover_container/popover_container.js"]
    asset_spec = "solute.epfl.components:popover_container/static"

    css_name = ["popover_container.css"]
    js_name = ["popover_container.js"]

    compo_config = []
    compo_state = ["title", "position", "label", "icon"]

    title = None  # : if title is none it is not displayed
    position = "top"  # : posible positions are top,left,right,bottom
    #: An optional font-awesome icon that should be displayed on the button.
    # Either the :attr:`icon` or the :attr:`label` have to be defined in order to yield a reasonable button.
    icon = None
    #: An optional label that should be displayed on the button.
    # Either the :attr:`icon` or the :attr:`label` have to be defined in order to yield a reasonable button.
    label = None
        
