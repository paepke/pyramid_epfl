epfl.init_component("{{ compo.cid }}", "Download", {"event_name" : "{{ compo.event_name }}",
                                                    "event_target" : {{ compo.event_target|tojson }},
                                                    "confirm_first": {{ compo.confirm_first|format_bool }},
                                                    "confirm_message": {{ compo.confirm_message|tojson }} });
