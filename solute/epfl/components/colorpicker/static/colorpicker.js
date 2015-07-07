epfl.ColorPicker = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
    $('#' + cid + ' [data-toggle="tooltip"]').tooltip();
};
epfl.ColorPicker.inherits_from(epfl.FormInputBase);

epfl.ColorPicker.prototype.handle_local_click = function (event) {
    epfl.FormInputBase.prototype.handle_local_click.call(this, event);

    var value = null;
    var target = $(event.target);
    if (target.hasClass("epfl-colorpicker-specialfield") ||
            target.hasClass("epfl-colorpicker-colorfield")) {
        value = target.data("value");
    } else if (target.hasClass("fa")) {
        value = target.parent().data("value");
    }

    if (value !== null) {
        epfl.send(epfl.make_component_event(this.cid, "change", {
            "value": value
        }));
    }

};
