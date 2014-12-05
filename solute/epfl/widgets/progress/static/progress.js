epfl.ProgressWidget = function(wid, cid, params) {
    var notify_epfl = function(){
        widget_obj.notify_value_change.call(widget_obj);
        if (widget_obj.get_param("on_change")) {
            var ev = widget_obj.make_event("onChange");
            epfl.send(ev);
        };
    }

    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);
    /*
    var field = $("#" + this.wid);
    var spinner_options = {}
    var options = params.params;

    if (options.step) {
        spinner_options.step = options.step;
    }

    if (options.min) {
        spinner_options.min = options.min;
    }

    if (options.max) {
        spinner_options.max = options.max;
    }

    field.spinner(spinner_options);
    */
    field.change(function() {
        notify_epfl();
    });
    /*
    field.on("spinstop", function(event, ui) {
        notify_epfl();
    });
    */
};
epfl.ProgressWidget.inherits_from(epfl.WidgetBase);

epfl.ProgressWidget.prototype.get_value = function() {
    return $("#" + this.wid).val();
};
