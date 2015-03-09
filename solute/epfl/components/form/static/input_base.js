epfl.FormInputBase = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var selector = "#" + cid;
    var compo_col = parseInt(params["compo_col"]);
    if ($(selector + " > label").length > 0) {
        $(selector + " > label").first().addClass("col-sm-1");
        compo_col -= 1;
    }
    $(selector+ " > div").first().addClass("col-sm-" + compo_col);
};

epfl.FormInputBase.event_change = function (cid, value, enqueue_event) {
    enqueue_event = enqueue_event || true;

    epfl.dispatch_event(cid, "set_dirty", {});
    if (enqueue_event) {
        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: value}), cid);
    } else {
        epfl.dispatch_event(cid, "change", {value: value});
    }
}

epfl.FormInputBase.on_change = function (compo, value, cid, enqueue_event) {
    if (value !== compo.lastValue) {
        compo.lastValue = value;
        epfl.FormInputBase.event_change(cid, value, enqueue_event);
    }
}


epfl.FormInputBase.inherits_from(epfl.ComponentBase);

