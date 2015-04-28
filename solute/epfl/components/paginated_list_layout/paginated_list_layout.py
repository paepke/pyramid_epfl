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

    search_focus = False

    theme_path = ['pretty_list_layout/theme', '<paginated_list_layout/theme']

    js_parts = PrettyListLayout.js_parts + ["paginated_list_layout/paginated_list_layout.js"]
    js_name = PrettyListLayout.js_name + [(
                                              'solute.epfl.components:paginated_list_layout/static',
                                              'paginated_list_layout.js'
                                          )]

