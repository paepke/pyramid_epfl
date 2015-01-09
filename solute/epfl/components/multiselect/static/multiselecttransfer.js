epfl.MultiSelectTransferComponent = function (cid, params) {
    var compo = this;
    epfl.ComponentBase.call(this, cid, params);
    $('[epflid="'+cid+'"]').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	var ev = compo.make_event("transfer",{});
    	epfl.send(ev);
    });
};
epfl.MultiSelectTransferComponent.inherits_from(epfl.ComponentBase);
