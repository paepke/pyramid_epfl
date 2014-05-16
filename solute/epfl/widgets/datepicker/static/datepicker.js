epfl.DatepickerWidget = function(wid, cid, params) {
    var widget_obj = this;

    $.datepicker.regional['de'] = {
        clearText: 'löschen',
        clearStatus: 'aktuelles Datum löschen',
        closeStatus: 'ohne Änderungen schließen',
        prevText: '&#x3c;zurück',
        prevStatus: 'letzten Monat zeigen',
        nextText: 'Vor&#x3e;',
        nextStatus: 'nächsten Monat zeigen',
        currentText: 'heute',
        currentStatus: '',
        monthNames: ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'],
        monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun','Jul','Aug','Sep','Okt','Nov','Dez'],
        monthStatus: 'anderen Monat anzeigen',
        yearStatus: 'anderes Jahr anzeigen',
        weekHeader: 'Wo',
        weekStatus: 'Woche des Monats',
        dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
        dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
        dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
        dayStatus: 'Setze DD als ersten Wochentag',
        dateStatus: 'Wähle D, M d',
        dateFormat: 'dd.mm.yy',
        firstDay: 1,
        initStatus: 'Wähle ein Datum',
        isRTL: false
    };

    $.datepicker.setDefaults($.datepicker.regional['de']);

    epfl.WidgetBase.call(this, wid, cid, params);

    var field = $("#" + this.wid);
    var datepicker_options = {};
    var options = params.params;

    if(options.default_date) {
        field.val(options.default_date);
        datepicker_options.defaultDate = options.default_date;
    }

    if(options.min_date) {
        datepicker_options.minDate = options.min_date;

    }

    if(options.max_date) {
        datepicker_options.maxDate = options.max_date;
    }

    field.datepicker(datepicker_options);

    field.change(function() {
        widget_obj.notify_value_change.call(widget_obj);
        if (widget_obj.get_param("on_change")) {
            var ev = widget_obj.make_event("onChange");
            epfl.send(ev);
        };
    });
};
epfl.DatepickerWidget.inherits_from(epfl.WidgetBase);

epfl.DatepickerWidget.prototype.get_value = function() {
    return $( "#" + this.wid).val();
};