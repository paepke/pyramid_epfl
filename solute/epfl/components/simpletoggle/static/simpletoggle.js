epfl.SimpleToggle = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var old_value = $(input_field).val();
    var input_field = "#" + cid + "_input";
    var input_button = "#" + cid + "_button";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    $(input_button).click(function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        event.stopPropagation();
        var old_value = $(input_field).val();
        if (old_value == "True") {
            $(input_field).val("False");
            $(input_button).
                    find("i").
                    removeClass("fa-" + params["enabled_icon"]).
                    removeClass("fa-" + params["enabled_icon_size"]).
                    removeClass("text-" + params["enabled_icon_color"]).
                    addClass("fa-" + params["disabled_icon"]).
                    addClass("fa-" + params["disabled_icon_size"]).
                    addClass("text-" + params["disabled_icon_color"]);
        }else{
            $(input_field).val("True");
            $(input_button).
                    find("i").
                    removeClass("fa-" + params["disabled_icon"]).
                    removeClass("fa-" + params["disabled_icon_size"]).
                    removeClass("text-" + params["disabled_icon_color"]).
                    addClass("fa-" + params["enabled_icon"]).
                    addClass("fa-" + params["enabled_icon_size"]).
                    addClass("text-" + params["enabled_icon_color"]);
        }
        var val = ($(input_field).val() == "True");
        epfl.FormInputBase.on_change(compo, val, cid, enqueue_event);
    });
};

epfl.SimpleToggle.inherits_from(epfl.ComponentBase);
