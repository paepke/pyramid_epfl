
epfl.FormComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    this.widgets = {};

    this.get_el().bind('keypress keydown keyup', function(e){
       if(e.keyCode == 13) { e.preventDefault(); }
    });
}; 
epfl.FormComponent.inherits_from(epfl.ComponentBase);

epfl.FormComponent.prototype.init_widget = function(wid, widget_class, params) {
	var constructor = epfl[widget_class];
	var widget_obj = new constructor(wid, this.cid, params);
	this.widgets[wid] = widget_obj;
};

epfl.FormComponent.prototype.add_tooltip = function(dom_id, msg) {
	var ui_tooltip_opts = { };
	$("#" + dom_id).attr('title', msg).tooltip(ui_tooltip_opts);
};

epfl.FormComponent.prototype.submit_form = function(submitting_element_id) {
	this.add_hidden("__submitting_element_id__", submitting_element_id);
	this.add_hidden("__tid__", epfl.tid);
	this.remove_all_value_change_events();
	this.get_form_el().submit();
};

epfl.FormComponent.prototype.add_hidden = function(name, value) {
	var form_obj = this.get_form_el();

	var hidden_field = $("<input>").attr({"type": "hidden",
	                   					  "name": name,
	                   					  "value": value});
	form_obj.append(hidden_field);
};

epfl.FormComponent.prototype.get_form = function() {
	return epfl.components[this.cid];
};

epfl.FormComponent.prototype.get_form_el = function() {
	return $("#" + this.cid);
};

epfl.FormComponent.prototype.remove_all_value_change_events = function() {
	for (wid in this.widgets) {
		var widget_obj = this.widgets[wid];
		widget_obj.remove_value_change_events();
	}
};