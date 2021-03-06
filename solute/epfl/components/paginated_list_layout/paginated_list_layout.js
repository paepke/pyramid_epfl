epfl.init_component("{{ compo.cid }}", "PaginatedListLayout", {
    'row_offset': {{ compo.row_offset|int }},
    'row_limit': {{ compo.row_limit|int }},
    'row_count': {{ compo.row_count|int }},
    'row_data': {{ compo.row_data|tojson }},
    'show_pagination': {{ compo.show_pagination|format_bool }},
    'show_search': {{ compo.show_search|format_bool }},
    'search_focus': {{ compo.search_focus|format_bool }}
});
