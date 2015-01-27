epfl.MultiSelectTransferComponent = function (cid, params) {
    var compo = this;
    epfl.ComponentBase.call(this, cid, params);
    $('[epflid="'+cid+'"]').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	epfl.dispatch_event(cid, "transfer", {});
    });
};
epfl.MultiSelectTransferComponent.inherits_from(epfl.ComponentBase);
