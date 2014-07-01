epfl.DatetimepickerWidget = function(wid, cid, params) {

    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    var field = $("#" + this.wid);
    var datetimepicker_options = {}
    var options = params.params;



    if(options.datepicker) {
        datetimepicker_options.datepicker = options.datepicker;
    }

    if(options.timepicker) {
        datetimepicker_options.timepicker = options.timepicker;
    }

    if(options.minDate) {
        datetimepicker_options.minDate = options.minDate;
    }

    if(options.maxDate) {
        datetimepicker_options.maxDate = options.maxDate;
    }

    if(options.minTime) {
        datetimepicker_options.minTime = options.minDate;
    }

    if(options.maxTime) {
        datetimepicker_options.maxTime = options.maxDate;
    }

    if(options.allowTimes) {
        datetimepicker_options.allowTimes = options.allowTimes;
    }

    if(options.step) {
        datetimepicker_options.step = options.step;
    }

    if(options.startDate) {
        datetimepicker_options.startDate = options.startDate;
    }


    field.datetimepicker(datetimepicker_options);

    field.change(function() {
        widget_obj.notify_value_change.call(widget_obj);
        if (widget_obj.get_param("on_change")) {
            var ev = widget_obj.make_event("onChange");
            epfl.send(ev);
        };
    });


};
epfl.DatetimepickerWidget.inherits_from(epfl.WidgetBase);

epfl.DatetimepickerWidget.prototype.get_value = function() {
    return $( "#" + this.wid).val();
};
