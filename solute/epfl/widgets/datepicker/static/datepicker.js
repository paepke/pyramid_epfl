epfl.init_datepicker_widget = function(params) {
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

    $(document).ready(function() {
        var field = $("#" + params.name + "__label");

        var datepicker_options = {};

        if(params.default_date) {
            field.val(params.default_date);
            datepicker_options.defaultDate = params.default_date;
        }

        if(params.min_date) {
            datepicker_options.minDate = params.min_date;
        }

        if(params.max_date) {
            datepicker_options.maxDate = params.max_date;
        }

        field.datepicker(datepicker_options);
    });
}