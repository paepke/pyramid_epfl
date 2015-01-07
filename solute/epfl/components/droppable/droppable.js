epfl.init_component("{{compo.cid}}",
                        "DroppableComponent",
                        {type: {{ compo.get_valid_types(True)|safe }}});
{% if compo.deactivate_on_drop %}
children = $("#{{compo.cid}}").children(".ui-sortable-handle");
if (children.length > 1) {
	$("#{{compo.cid}}").sortable("disable");
}                
$("#{{compo.cid}}").on('sortstop', function (event, ui) {
            $("#{{compo.cid}}").sortable("disable");
        });
{% endif %}