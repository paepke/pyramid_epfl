

epfl.ComponentBase = function(cid, params) { ;
	this.cid = cid;
	this.params = params;
};

epfl.ComponentBase.prototype.get_el = function(part) {
	if (part) {
		var el = $("[epflid='" + this.cid + "$" + part + "']");
	} else {
		var el = $("[epflid='" + this.cid + "']");		
	}
	return el;
};

epfl.ComponentBase.prototype.make_event = function(event_name, params) {
//	return epfl.make_component_event(this.cid, event_name, params, needs_ack);
	return epfl.make_component_event(this.cid, event_name, params);
};

epfl.ComponentBase.prototype.destroy = function() {
};

