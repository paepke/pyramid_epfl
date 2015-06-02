epfl.init_component("{{ compo.cid }}", "SimpleToggle", {
    "fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
    "enabled_icon":{{ compo.enabled_icon|tojson }},
    "disabled_icon":{{ compo.disabled_icon|tojson }},
    "enabled_icon_size":{{ compo.enabled_icon_size|tojson }},
    "disabled_icon_size":{{ compo.disabled_icon_size|tojson }},
    "enabled_icon_color":{{ compo.enabled_icon_color|tojson }},
    "disabled_icon_color":{{ compo.disabled_icon_color|tojson }}
});
