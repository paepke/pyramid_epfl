epfl.TextInput = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
    };

    var elm = $(selector);

    if (elm.val() != elm.attr('data-initial-value')) {
        change();
    }

    elm.blur(change).change(change);
};

epfl.TextInput.inherits_from(epfl.FormInputBase);
