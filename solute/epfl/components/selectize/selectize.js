epfl.init_component("{{ compo.cid }}", "Selectize", {
    "fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
    "search_server_side":{{compo.search_server_side|format_bool}},
    "search_text":{{ compo.search_text|tojson }},
    "input_focus":{{ compo.input_focus | format_bool }},
    "cursor_position": {{ compo.cursor_position }},
    "selected_text":{{ compo.selected_text|tojson }}
});

