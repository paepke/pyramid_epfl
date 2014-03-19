
epfl.BasicWidget = function(wid, cid, params) {

	var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

	this.typ = params.typ;

	if (this.typ == "button") {

		// Javascript for buttons
        if (this.get_param("on_click") == "submit") {
            $("#" + this.wid).click(function() {
            	var compo = widget_obj.get_form();
                compo.submit_form.call(compo, this.id);
            });            
        } else if (this.get_param("on_click")) {
            $("#" + this.wid).click(function() {
                var ev = widget_obj.make_event("onClick", {});
                epfl.send(ev);
            });            
        }

    } else if (this.typ == "entry") {

        // Javascript for entry-fields
        $("#" + this.wid).change(function() {
            widget_obj.notify_value_change.call(widget_obj);
        });            

    } else if (this.typ == "textarea") {

        // Javascript for textarea-fields
        $("#" + this.wid).change(function() {
            widget_obj.notify_value_change.call(widget_obj);
        });            

    } else if (this.typ == "select") {

        // Javascript for select-fields
        $("#" + this.wid).change(function() {
            widget_obj.notify_value_change.call(widget_obj);
            if (widget_obj.get_param("on_change")) {
                var ev = widget_obj.make_event("onChange");
                epfl.send(ev);
            };
        });            

    }

};
epfl.BasicWidget.inherits_from(epfl.WidgetBase);



epfl.BasicWidget.prototype.get_value = function() {
    return $( "#" + this.wid).val();
};