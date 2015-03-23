epfl.TextInput = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var max_length = params["max_length"];
    var show_count = params["show_count"];
    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
        if(show_count && max_length){
            $(selector + '_count').text($(selector).val().length);
        }
    };

    $(selector).blur(change).change(change).keydown(change);
};

epfl.TextInput.inherits_from(epfl.ComponentBase);
