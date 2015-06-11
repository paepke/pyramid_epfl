# coding: utf-8

"""

"""

from solute.epfl.components import ListLayout


class PrettyListLayout(ListLayout):

    asset_spec = "solute.epfl.components:pretty_list_layout/static"
    theme_path = ListLayout.theme_path + ["pretty_list_layout/theme"]

    #: The max height of the list view. If the entries exceed the height, a scrollbar is displayed.
    height = None

    css_name = ListLayout.css_name + \
        [("solute.epfl.components:pretty_list_layout/static", "pretty_list_layout.css")]

    def __init__(self, page, cid, height=None, **kwargs):
        """ContainerComponent using Bootstrap to prettify the output like a list.

        :param height: Set the list to the given height in pixels.
        """
        super(PrettyListLayout, self).__init__(page, cid, height=height, **kwargs)
