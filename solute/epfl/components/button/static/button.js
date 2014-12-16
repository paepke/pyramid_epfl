epfl.ButtonComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    $('#'+this.cid).click(function() {
        params = {}
        var evt = compo.make_event("on_click", params);
        epfl.send(evt);
    });
};
epfl.ButtonComponent.inherits_from(epfl.ComponentBase);

epfl.ButtonComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn);
};
