
epfl.init_slider_widget = function(params) {
	$(document).ready(function() {

		function show_value(value) {
			if (params["value_divisor"] == 1) {
				value = parseInt(value);
			} else {
				value = value.toFixed(2);
			}
			$("#" + params.name + "_value_box").html(value);
		};

		var value = parseFloat($("#" + params.name).val());
		show_value(value);
		var slider = $("#" + params.name + "_slider").slider({

			min: params.min,
			max: params.max,
			value: value * params["value_divisor"],
			
			slide: function(event, ui) {
				var value = ui.value / params["value_divisor"];
				show_value(value);
			},
			change: function(event, ui) {
				var value = ui.value / params["value_divisor"];
				$("#" + params.name).val(value);
				show_value(value);
				if (params.on_change == "submit") {
					$("#" + params.name).closest("form").submit();
				} else if (params.on_change) {
					var event = epfl.make_component_event(params.cid, params.on_change, {"widget_name": params.name,
																					     "value": value});
					epfl.send(event);
				};
			}
		});
	});
};
