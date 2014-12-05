epfl.ToggleWidget = function(wid, cid, params) {
    var notify_epfl = function(){
        widget_obj.notify_value_change.call(widget_obj);
        if (widget_obj.get_param("on_change")) {
            var ev = widget_obj.make_event("onChange");
            epfl.send(ev);
        };
    }

    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);
    
    var field = $("#" + this.wid);

    field.on('switchChange.bootstrapSwitch', function(event, state) {
        notify_epfl();
    });
    
};
epfl.ToggleWidget.inherits_from(epfl.WidgetBase);

epfl.ToggleWidget.prototype.get_value = function() {
    return $("#" + this.wid).is(":checked");
};
