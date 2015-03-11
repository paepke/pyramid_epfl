epfl.FormInputBase = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var addCustomStyle = function (element, style) {
        if(style !== "None"){
            element.attr('style', style);
        }
    };

    var selector = "#" + cid;
    var compo_col = parseInt(params["compo_col"]);
    var label_col = parseInt(params["label_col"]);
    var vertical = params["vertical"];

    if (vertical === true) {
        if ($(selector).children().first().prop("tagName") === "LABEL") {
            addCustomStyle($(selector).children().first(), params["label_style"]);
            $(selector).children().first().wrap("<div class='row'></div>").wrap("<div class='col-sm-" + compo_col + "'></div>");
        }
        $(selector).children().eq(1).addClass("col-sm-" + compo_col);
        $(selector).children().eq(1).wrap("<div class='row'></div>");
    } else {
        if ($(selector).children().first().prop("tagName") === "LABEL") {
            addCustomStyle($(selector).children().first(), params["label_style"]);
            $(selector).children().first().addClass("col-sm-" + label_col);
            compo_col -= parseInt(label_col);
        }
        $(selector + " > div").first().addClass("col-sm-" + compo_col);
    }

    addCustomStyle($(selector + " input"),params["input_style"]);
};

epfl.FormInputBase.event_change = function (cid, value, enqueue_event) {
    if (enqueue_event === undefined) {
        enqueue_event = true;
    }

    if (enqueue_event) {
        epfl.dispatch_event(cid, "set_dirty", {});
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

