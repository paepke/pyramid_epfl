from solute.epfl.components.grouped_link_list_layout.grouped_link_list_layout import GroupedLinkListLayout


class TypeAhead(GroupedLinkListLayout):
    search_focus = True  #: Focus on the search input field on load.
    show_search = True  #: Show the search input field.
    use_headings = True  #: Sets GroupedLinkListLayout to show headings instead of submenus.

    js_parts = []
    js_name = GroupedLinkListLayout.js_name + [('solute.epfl.components:typeahead/static', 'typeahead.js')]

    new_style_compo = True
    compo_js_name = 'TypeAhead'
    compo_js_params = ['row_offset', 'row_limit', 'row_count', 'row_data', 'show_pagination', 'show_search',
                       'search_focus']
    compo_js_extras = ['handle_click']

    theme_path = GroupedLinkListLayout.theme_path.copy()
    theme_path['before'] = ['pretty_list_layout/theme', '>paginated_list_layout/theme', '>typeahead/theme']

    data_interface = {
        'id': None,
        'text': None
    }

    def __init__(self, page, cid, **kwargs):
        """TypeAhead component that offers grouping of entries under a common heading.

        components.TypeAhead(
            cols=3,
            cid='target_log',
            event_name='selected_category',
            links=[
                {'text': 'foo0', 'url': '#foo', 'menu_group': 'bar'},
                {'text': 'foo1', 'url': '#foo', 'menu_group': 'bar'},
                {'text': 'foo2', 'url': '#foo', 'menu_group': 'bar2'},
                {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
                {'text': 'foo3', 'url': '#foo', 'menu_group': 'bar2'},
            ]
        )


        """
