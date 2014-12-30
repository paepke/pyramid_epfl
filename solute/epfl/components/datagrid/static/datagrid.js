epfl.DataGridComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    console.log("MOEP");
    var ev = this.make_event("getdata",{});
    epfl.send(ev);
};
epfl.DataGridComponent.inherits_from(epfl.ComponentBase);

epfl.DataGridComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

