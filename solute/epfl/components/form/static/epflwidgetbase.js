

epfl.WidgetBase = function(wid, form_cid, params) {
	this.form_cid = form_cid;
	this.params = params;
	this.wid = wid;
	this.name = params.name;
};

epfl.WidgetBase.prototype.get_form = function() {
	return epfl.components[this.form_cid];
};

epfl.WidgetBase.prototype.get_form_el = function() {
	return $("#" + this.form_cid);
};

epfl.WidgetBase.prototype.get_param = function(name) {
	return this.params.params[name];
};

epfl.WidgetBase.prototype.make_event = function(cmd, params) {
	if (typeof params == "undefined") { params = {} };
    params["widget_name"] = this.name;
	return this.get_form().make_event(cmd, params);
};

epfl.WidgetBase.prototype.notify_value_change = function() {
	var new_value = this.get_value();
	var ev = this.make_event("ValueChange", {"value": new_value});
	epfl.repeat_enqueue(ev, this.wid + "/vc");
};


epfl.WidgetBase.prototype.remove_value_change_events = function() {
	epfl.dequeue(this.wid + "/vc");
};