epfl.FormInputBase = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var addCustomStyle = function (element, style) {
        if(style !== "None"){
            element.attr('style', style);
        }
    };

    var selector = "#" + cid;
    addCustomStyle($(selector + " input"),params["input_style"]);
};

epfl.FormInputBase.event_change = function (cid, value, enqueue_event) {
    if (enqueue_event === undefined) {
        enqueue_event = true;
    }

    if (enqueue_event) {
        epfl.repeat_enqueue(epfl.make_component_event(cid, 'set_dirty', {}), cid);
        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: value}), cid);
    } else {
        epfl.repeat_enqueue(epfl.make_component_event(cid, 'set_dirty', {}), cid);
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

