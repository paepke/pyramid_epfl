# coding: utf-8

from solute.epfl.core import epflcomponentbase


class ColLayout(epflcomponentbase.ComponentContainerBase):

    """

    A layout component that renders child components as cols (using Bootstrap's col layout).

    Use it like this:

    .. code:: python

        col_layout = ColLayout(
            node_list=[
                Text(value="Text 1", cols=6),
                Text(value="Text 2 centered", cols=6, align="center")
            ]
        )


    Every child component is required to have the cols attribute indicating the number of cols it
    should use. The cols attribute must a number between 1 and 12.
    A child component can also optionally have the align attribute ("left", "right" or "center"),
    indicating that it should be aligned in a certain way.

    """

    asset_spec = "solute.epfl.components:col_layout/static"
    css_name = ["col_layout.css"]

    template_name = "col_layout/col_layout.html"
    vertical_center = False  #: If set to true, child components are centered vertically.

    def __init__(self, page, cid, vertical_center=False, **extra_params):
        """
        A layout component that renders child components as cols (using Bootstrap's col layout).

        Every child component is required to have the cols attribute indicating the number of cols it
        should use. The cols attribute must a number between 1 and 12.
        A child component can also optionally have the text_center attribute (boolean), indicating
        that it should be centered horizontally.

        :param vertical_center: If set to true, child components are centered vertically
        """
        super(ColLayout, self).__init__(
            page=page, cid=cid,
            vertical_center=vertical_center,
            **extra_params)
