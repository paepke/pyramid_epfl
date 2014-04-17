
epfl.CanvasComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);

}; 
epfl.CanvasComponent.inherits_from(epfl.ComponentBase);

epfl.CanvasComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) { params = {} };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};
