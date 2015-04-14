epfl.init_component("{{ compo.cid }}", "DownloadComponent", {"event_name" : "{{ compo.event_name }}",
														     "event_target" : "{{ compo.event_target }}",
														     "confirm_first": {{ compo.confirm_first|format_bool }},
														     "confirm_message": "{{ compo.confirm_message }}" });
