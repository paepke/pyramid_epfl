epfl.FormInputBase = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    var compo_cid = cid;
    var selector = "#" + cid;
    var type = $(selector).closest("div").attr('epfl-type');
    var fire_change_immediately = params["fire_change_immediately"];
    
    function event_change(value) {
    	epfl.dispatch_event(cid, "set_dirty", {});
		if (fire_change_immediately) {
            epfl.dispatch_event(cid, "change", {value: value});
        } else {
            epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: value}), cid);
        }
    }


    if (type == "defaultinput" || type == "textarea") {
        var inputType = $(selector).attr("type");

        $(selector).keyup(function (event) {
            if ($(selector).val() !== compo.lastValue) {
                compo.lastValue = $(selector).val();
                event_change($(selector).val());
            }
        }).keydown(function(event){
            if (inputType === "number" &&
                (event.keyCode < 48 || event.keyCode > 57) &&
                [190, 46, 8, 9, 27, 13, 110, 35, 36, 37, 38, 39, 40].indexOf(event.keyCode) === -1) {
                if(compo.ctrl && [65,67,86,88].indexOf(event.keyCode) !== -1){
                }else {
                    compo.ctrl = event.ctrlKey;
                    event.preventDefault();
                    return;
                }
            }
        });

        provide_typeahead = $(selector).data("provide");
        if (provide_typeahead == "typeahead") {
            $(selector).typeahead({
                source: function (query, process) {
                    epfl.dispatch_event(cid, "typeahead", {"query": query});
                    // todo: results have to be returned from server
                    return process(['Amsterdam', 'Washington', 'Sydney', 'Beijing', 'Cairo']);
                }
            });
        }

    } else if (type == "select") {
        $(selector).change(function () {
            event_change($(selector).val());
        });
    } else if (type == "checkbox") {
        $(selector).attr('checked', $(selector).val() == 'True');
        $(selector).change(function () {
            var val = val = $(this).is(':checked');
            event_change(val);
        });

    } else if (type == "toggle") {
        $(selector).attr('checked', $(selector).val() == 'True');
        $(selector).bootstrapSwitch('state');
        $(selector).on('switchChange.bootstrapSwitch', function (event, state) {
            var val = $(this).closest("div").parent().hasClass("bootstrap-switch-on");
            event_change(val);
        });

    } else if (type == "radiobuttongroup") {

        selector = "input[type=radio][name=" + cid + "]";
        $(selector).change(function () {
            var val = $(this).val();
            event_change(val);
        });

    } else if (type == "buttonsetgroup") {
        selector = "input[type=radio][name=" + cid + "]";
        $(selector).change(function () {
            var val = $(this).val();
            event_change(val);
        });
    }
    if (params["submit_form_on_enter"]) {
        $(selector).bind('keyup', function (event) {
            if (event.keyCode == 13) {
                epfl.dispatch_event(cid, "submit", {}); // bubbles up to form
            }
        });
    }
    if (params["input_focus"]) {
        $(selector).focus();
    }

};
epfl.FormInputBase.inherits_from(epfl.ComponentBase);

