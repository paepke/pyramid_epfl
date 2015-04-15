epfl.MultiSelectTransfer = function (cid, params) {
    var compo = this;
    epfl.ComponentBase.call(this, cid, params);
    $('#'+cid).click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	epfl.dispatch_event(cid, "transfer", {});
    });
};
epfl.MultiSelectTransfer.inherits_from(epfl.ComponentBase);
