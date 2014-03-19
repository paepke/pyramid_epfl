
epfl.AutoCompleteWidget = function(wid, cid, params) {

	var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    $("#" + wid + "__entry").autocomplete({
    	source: function(request, response) {

    		$("#" + wid).val("");

    		var event = widget_obj.make_event("GetData", {"query": request.term});
    		epfl.send(event, function(data) {
    			if (data.length == 1) {
    				$('#' + wid + "__entry").val(data[0].label);
    				$('#' + wid).val(data[0].value);
    			};
    			response(data);
    		});

    	},
    	minLength: 2,
    	select: function(event, ui) {
    		var sel_obj = ui.item;
    		$('#' + wid + "__entry").val(sel_obj.label);
    		$('#' + wid).val(sel_obj.value);
            widget_obj.notify_value_change();
    		return false;
    	},
    	focus: function(event, ui) {
    		var sel_obj = ui.item;
    		$('#' + wid + "__entry").val(sel_obj.label);
    		$('#' + wid).val(sel_obj.value);
            widget_obj.notify_value_change();
    		return false;
    	}
    });

    $("#" + wid + "__entry").change(function() {
        widget_obj.notify_value_change();
    });

};
epfl.AutoCompleteWidget.inherits_from(epfl.WidgetBase);



epfl.AutoCompleteWidget.prototype.get_value = function() {
    return {"value": $( "#" + this.wid).val(),
            "entry": $( "#" + this.wid + "__entry").val()}
};

