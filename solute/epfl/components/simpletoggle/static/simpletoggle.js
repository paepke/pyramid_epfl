epfl.SimpleToggle = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    
	var input_field = "#" + cid + "_input";
    var input_button = "#" + cid + "_button";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    $(input_button).click(function(event) {
        event.stopImmediatePropagation();
        event.preventDefault();
        event.stopPropagation();
        var old_value = $(input_field).val();
        if (old_value == "True") {
            $(input_field).val("False");
            
            $(input_button).find("i").removeClass("fa-toggle-on text-primary").addClass("fa-toggle-off");
        } else {
            $(input_field).val("True");
            $(input_button).find("i").removeClass("fa-toggle-off").addClass("fa-toggle-on text-primary");
        }
        var val = ($(input_field).val() == "True"); 
        epfl.FormInputBase.on_change(compo, val, cid, enqueue_event);
    });
};

epfl.SimpleToggle.inherits_from(epfl.ComponentBase);
