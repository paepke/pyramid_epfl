# coding: utf-8

"""

"""

from solute.epfl.components import PrettyListLayout


class PaginatedListLayout(PrettyListLayout):
    """
    A searchable list layout. Its content is configured using get_data()
    example

    .. code-block:: python

        data = []
        for i in range(0, 100):
            data.append({'id': i, "data": "test" + str(i)})

    """

    show_pagination = True  #: Set to true to show the pagination bar.
    show_search = True  #: Set to true to enable the search field.

    search_focus = False  #: Set to true if the search field should receive focus on load.

    theme_path = ['pretty_list_layout/theme', '<paginated_list_layout/theme']

    js_parts = PrettyListLayout.js_parts + ["paginated_list_layout/paginated_list_layout.js"]
    js_name = PrettyListLayout.js_name + [(
                                              'solute.epfl.components:paginated_list_layout/static',
                                              'paginated_list_layout.js'
                                          )]

    def __init__(self, page, cid, show_search=None, height=None, **kwargs):
        """Paginated list using the PrettyListLayout based on bootstrap. Offers searchbar above and pagination below
        using the EPFL theming mechanism.

        :param height: Set the list to the given height in pixels.
        :param show_search: Toggle weather the search field is shown or not.
        :param show_pagination: Toggle weather the pagination is shown or not.
        :param search_focus: Toggle weather the search field receives focus on load or not.
        """
        super(PaginatedListLayout, self).__init__(page, cid, show_search=None, height=height, **kwargs)
