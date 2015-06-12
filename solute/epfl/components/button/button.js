epfl.init_component("{{ compo.cid }}", "Button", {"event_name" : "{{ compo.event_name }}",
                                                  "event_target" : "{{ compo.event_target }}",
                                                  "confirm_first": {{ compo.confirm_first|format_bool }},
                                                  "confirm_message": "{{ compo.confirm_message }}",
                                                  "disable_on_click": {{ compo.disable_on_click|format_bool }},});
