epfl.ButtonComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var confirm_first=params["confirm_first"];
    var confirm_message=params["confirm_message"];
    var event_name=params["event_name"];
    var event_target=params["event_target"];
	$('#' + cid + ' div button').click(function(event) {
		if (confirm_first && (!confirm(confirm_message))) {
			return;
		}
	    var request = epfl.make_component_event(event_target, event_name);
	    epfl.send(request);
	});

};
epfl.ButtonComponent.inherits_from(epfl.ComponentBase);
