epfl.ColorPicker = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
    $('#' + cid + ' [data-toggle="tooltip"]').tooltip();
     console.log("RELOAD");
};
epfl.ColorPicker.inherits_from(epfl.FormInputBase);

epfl.ColorPicker.prototype.handle_local_click = function (event) {
    console.log("CLICK");
    epfl.FormInputBase.prototype.handle_local_click.call(this, event);

    var value = null;

    if ($(event.target).hasClass("epfl-colorpicker-specialfield") ||
            $(event.target).hasClass("epfl-colorpicker-colorfield")) {
        value = $(event.target).data("value");
    } else if ($(event.target).hasClass("fa fa-code fa-lg")) {
        value = $(event.target).parent().data("value");
    }

    if (value !== null) {
        epfl.send(epfl.make_component_event(this.cid, "change", {
            "value": value
        }));
    }

};