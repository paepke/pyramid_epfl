epfl.BoxComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    $('[epflid="'+cid+'"] > .epfl_box_remove_button').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	var ev = compo.make_event("removed",{});
    	epfl.send(ev);
    });
    
};
epfl.BoxComponent.inherits_from(epfl.ComponentBase);
