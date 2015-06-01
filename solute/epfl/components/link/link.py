# coding: utf-8


from solute.epfl.core.epflcomponentbase import ComponentBase


class Link(ComponentBase):
    asset_spec = "solute.epfl.components:link/static"
    template_name = "link/link.html"
    js_name = ["link.js"]

    compo_state = ["url", "name"]
    
    url = '#'  #: The url this link points to. Used as src attribute of the A-Tag.
    name = 'Please change me!'  #: The name displayed for this link.

    def __init__(self, page, cid, url=None, name=None, **extra_params):
        """Simple Link component.

        Usage:
        .. code-block:: python

            Link(
                name="billiger.de",
                url="http://www.billiger.de"
            )

        :param url: The url this link points to. Used as src attribute of the A-Tag.
        :param name: The name displayed for this link.
        """
        super(Link, self).__init__(page, cid, url=url, name=name, **extra_params)


