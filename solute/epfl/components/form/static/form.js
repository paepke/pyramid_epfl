epfl.FormComponent = function (cid, params) {
	$('#'+cid).submit(function(event) {
	    event.preventDefault();
	    epfl.dispatch_event(cid, "submit", {});
	});
};
epfl.FormComponent.inherits_from(epfl.ComponentBase);