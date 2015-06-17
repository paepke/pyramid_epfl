epfl.LinkListLayout = function(cid, params) {
    epfl.PaginatedListLayout.call(this, cid, params);
};
epfl.LinkListLayout.inherits_from(epfl.PaginatedListLayout);

epfl.LinkListLayout.prototype.handle_click = function (event) {
    var target = $(event.target);
    console.log(event, target, this.params.event_name);
    if (this.params.event_name && target.attr('data-parent-epflid') == this.cid) {
        var evt = epfl.make_component_event(this.closest_cid(event.target), this.params.event_name);
        epfl.send(evt);
    }
};
