# coding: utf-8

from solute.epfl.components.link.link import Link

class Breadcrumb(Link):

    breadcrump=True  #: The link is used as a breadcrumb per default.

    def __init__(self, page, cid, url=None, name=None, icon=None, **extra_params):
        """Convenience component that can be used for creating breadcrumbs.

        Usage:
        .. code-block:: python

            self.page.breadcrumbs.add_component(
                components.Breadcrump(
                    name='Home',
                    url='/',
                    slot='left'
                )
            )

        :param url: The url the breadcrump points to. Used as src attribute of the A-Tag.
        :param name: The name displayed for this breadcrump.
        :param icon: The icon to be displayed in front of the text.
        """
        super(Breadcrumb, self).__init__(page, cid, url=url, name=name, **extra_params)
