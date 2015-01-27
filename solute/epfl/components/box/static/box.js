epfl.BoxComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $('[epflid="'+cid+'"] > .epfl_box_remove_button').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	epfl.dispatch_event(cid, "removed", {});
    });
    
};
epfl.BoxComponent.inherits_from(epfl.ComponentBase);
