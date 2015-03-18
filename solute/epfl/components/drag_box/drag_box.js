epfl.init_component("{{compo.cid}}", "DragBoxComponent", {});
{% if compo.disable_drag is None or (not compo.disable_drag) %}
epfl.make_compo_dragable("{{ compo.cid }}", {"keep_orig_in_place": {{ "false" if compo.keep_orig_in_place is None else compo.keep_orig_in_place|format_bool }}});
{% endif %}