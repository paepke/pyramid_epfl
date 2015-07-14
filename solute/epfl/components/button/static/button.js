epfl.Button = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Button.inherits_from(epfl.ComponentBase);

epfl.Button.prototype.handle_click = function(event) {
    var obj = this;
    var confirm_first = obj.params["confirm_first"];
    var confirm_message = obj.params["confirm_message"];
    var event_name = obj.params["event_name"];
    var event_target = obj.params["event_target"];
    var disable_on_click = obj.params["disable_on_click"];

    if (confirm_first && (!confirm(confirm_message))) {
        return;
    }
    if (disable_on_click) {
        $(this).addClass("disabled");
    }
    if(event_target){
        var request = epfl.make_component_event(event_target, event_name);
        epfl.send(request);
        return;
    }
    this.send_event(event_name, {});
};
