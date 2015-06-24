epfl.Link = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Link.inherits_from(epfl.ComponentBase);

epfl.Link.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);
    if (this.params.event_name) {
        this.send_event(this.params.event_name);
        event.originalEvent.preventDefault();
    }
};