epfl.FormInputBase = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var selector = "#" + cid;
    var compo_col = parseInt(params["compo_col"]);
    var label_col = parseInt(params["label_col"]);

    if ($(selector).children().first().prop("tagName") === "LABEL") {
        $(selector).children().first().addClass("col-sm-"+label_col);
        compo_col -= parseInt(label_col);
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

