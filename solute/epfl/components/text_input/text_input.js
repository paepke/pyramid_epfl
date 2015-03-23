epfl.init_component("{{compo.cid}}",
                    "TextInput", {"fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
                                  {% if compo.max_length is not none %}
                                    "max_length": {{ compo.max_length|int }},
                                  {% endif %}
                                  "show_count": {{ compo.show_count|format_bool }}});
