epfl.Form = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

	$('#'+cid).submit(function(event) {
	    event.preventDefault();
	    epfl.dispatch_event(cid, "submit", {});
	});
};
epfl.Form.inherits_from(epfl.ComponentBase);