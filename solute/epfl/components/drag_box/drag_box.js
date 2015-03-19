epfl.init_component("{{compo.cid}}", "DragBoxComponent", {});
{% if (not compo.disable_drag) %}
epfl.make_compo_dragable("{{ compo.cid }}", {"keep_orig_in_place": {{ "false" if compo.keep_orig_in_place is none else compo.keep_orig_in_place|format_bool }}});
{% endif %}