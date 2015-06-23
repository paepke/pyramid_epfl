# coding: utf-8


from solute.epfl.core.epflcomponentbase import ComponentBase


class Link(ComponentBase):
    asset_spec = "solute.epfl.components:link/static"
    template_name = "link/link.html"
    js_name = ["link.js"]
    css_name = ["link.css"]

    compo_state = ["url", "name"]
    
    route = None  #: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
    name = 'Please change me!'  #: The name displayed for this link.
    icon = None  #: The icon to be displayed in front of the text.
    breadcrumb = False  #: Display the link as a breadcrumb.
    tile = False  #: Display the link as a rectangular tile.

    new_style_compo = True
    compo_js_name = 'Link'

    def __init__(self, page, cid, url=None, route=None, name=None, icon=None, breadcrumb=None, tile=None, **extra_params):
        """Simple Link component.

        Usage:
        .. code-block:: python

            Link(
                name="billiger.de",
                url="http://www.billiger.de"
            )

        :param url: The url this link points to. Used as src attribute of the A-Tag. If present route will be ignored.
        :param route: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
        :param name: The name displayed for this link.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param tile: Display the link as a rectangular tile.
        """
        super(Link, self).__init__(page, cid, url=url, name=name, **extra_params)

    @property
    def url(self):
        if self.route is None:
            return
        return self.page.get_route_path(self.route)

    def is_first(self):
        """Returns True if the Link is the first component in this slot.
        """
        if not self.container_compo:
            return True
        siblings = self.container_compo.components
        position = siblings.index(self)
        if position == 0:
            return True

        for i in range(0, position):
            if siblings[position - 1 - i].slot == self.slot:
                return False

        return True
