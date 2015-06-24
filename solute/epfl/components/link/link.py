# coding: utf-8


from solute.epfl.core.epflcomponentbase import ComponentBase


class Link(ComponentBase):
    asset_spec = "solute.epfl.components:link/static"
    template_name = "link/link.html"
    js_name = ["link.js"]
    css_name = ["link.css"]

    compo_state = ["url", "route", "text", "icon", "name"]

    url = None  #: The url this link points to. Used for the src attribute of the A-Tag.
    route = None  #: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
    text = None  #: Alias for name.
    icon = None  #: The icon to be displayed in front of the text.
    breadcrumb = False  #: Display the link as a breadcrumb.
    tile = False  #: Display the link as a rectangular tile.
    list_element = False  #: Display the link as a bootstrap style list element.
    event_name = None  #: Name of an event to be triggered on click, prevents url and route from taking effect.

    new_style_compo = True
    compo_js_params = ['event_name']
    compo_js_name = 'Link'
    compo_js_extras = ['handle_click']

    def __init__(self, page, cid, url=None, route=None, name=None, text=None, icon=None, breadcrumb=None, tile=None,
                 list_element=None, event_name=None, selection=None, **extra_params):
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
        :param text: Alias for name.
        :param selection: Tuple of integers: (selection_start, selection_end). MARK-Tag will be applied there.
        :param icon: The icon to be displayed in front of the text.
        :param breadcrumb: Display the link as a breadcrumb.
        :param tile: Display the link as a rectangular tile.
        :param list_element: Display the link as a bootstrap style list element.
        :param event_name: Name of an event to be triggered on click, prevents url and route from taking effect.
        """
        super(Link, self).__init__(page, cid, url=url, route=route, name=name, text=text, icon=icon,
                                   breadcrumb=breadcrumb, tile=tile, list_element=list_element, event_name=event_name,
                                   **extra_params)

    @property
    def _url(self):
        if self.event_name:
            return

        if self.route is None:
            self.route = self.url
        if self.route is None:
            return

        try:
            return self.page.get_route_path(self.route)
        except KeyError:
            pass

        try:
            return self.page.get_route_path(self.route, **self.page.request.matchdict)
        except KeyError:
            pass

        try:
            return self.route.format()
        except KeyError:
            pass

        try:
            return self.route.format(**self.page.request.matchdict)
        except KeyError:
            return None

    @property
    def name(self):
        if not self.text and self.route:
            return self.route  # TODO: Lookup the route_text in EPFLView.
        return self.text

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

    def is_current_url(self):
        return self.page.request.matched_route.path == self._url
