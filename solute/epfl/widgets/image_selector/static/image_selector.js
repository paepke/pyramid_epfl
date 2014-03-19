
epfl.init_image_selector_widget = function(params) {
	$(document).ready(function() {
		$(".epfl_imgsel_" + params.name).click(function() {
			$(".epfl_imgsel_" + params.name).unhighlight_hover_border();
			$(this).highlight_hover_border();
			$("#" + params.name).val($(this).attr("item_id"));
			if (params.on_click == "submit") {
				$("#" + params.name).closest("form").submit();
			} else if (params.on_click) {
				var event = epfl.make_component_event(params.cid, params.on_click, {"widget_name": params.name, "value": $(this).attr("item_id")});
				epfl.send(event);
			};
		});
	});
}
