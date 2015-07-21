epfl.DatetimeInput = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
};
epfl.DatetimeInput.inherits_from(epfl.FormInputBase);

Object.defineProperty(epfl.DatetimeInput.prototype, 'input', {
    get: function () {
        return this.elm.find('input');
    }
});

epfl.DatetimeInput.prototype.DATE_FORMAT_LOCALE = "de";

epfl.DatetimeInput.prototype.after_response = function (data) {
    epfl.FormInputBase.prototype.after_response.call(this, data);

    this.input.datetimepicker({
        locale: 'de',
        format: this.params["date_format"],
        icons: {
            time: 'fa fa-clock-o',
            date: 'fa fa-calendar',
            up: 'fa fa-angle-up',
            down: 'fa fa-angle-down',
            previous: 'fa fa-angle-left',
            next: 'fa fa-angle-right',
            today: 'fa fa-crosshairs',
            clear: 'fa fa-trash',
            close: 'fa fa-times'
        },
        useCurrent:false

    }).blur(this.change.bind(this)).change(this.change.bind(this));

    if (this.params["value"] != null) {
        this.input.val(moment(this.params["value"]).locale(this.DATE_FORMAT_LOCALE).format(this.params["date_format"]));
    }

};

epfl.DatetimeInput.prototype.change = function (event) {
    var value = this.input.val();
    if(!value){
        return;
    }

    value = moment(value).locale(this.DATE_FORMAT_LOCALE).format();

    var enqueue_event = true;
    if (this.params.fire_change_immediately) {
        enqueue_event = false;
    }
    var parent_form = this.elm.closest('.epfl-form');
    if (parent_form.length == 1) {
        var is_dirty = parent_form.data('dirty');
        if (is_dirty == '0') {
            parent_form.data('dirty', '1');
            // first change to the form. always send event immediately so that
            // the serve can handle is_dirty change
            enqueue_event = false;

            this.repeat_enqueue('set_dirty', {}, this.cid + "_set_dirty");
        }
    }

    if (enqueue_event) {
        this.repeat_enqueue('change', {value: value}, this.cid + "_change");
    } else {
        this.send_event('change', {value: value});
    }
};

