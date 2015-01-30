epfl.init_component("{{compo.cid}}", "DragBoxComponent", {});
{% if not compo.disable_drag %}
epfl.make_compo_dragable("{{ compo.cid }}");
{% endif %}