epfl.FlipFlopComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.FlipFlopComponent.inherits_from(epfl.ComponentBase);

epfl.FlipFlopComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

