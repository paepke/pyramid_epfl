epfl.SimpleDroppableComponent = function (cid, params) {
    this.blocked = 0;
    var my_params =  params.type;
    epfl.ComponentBase.call(this, cid, params);
    
    $('[epflid="'+cid+'"] > .simpledroppable').droppable({
		accept: function(elem) {
			for (var i = 0; i < my_params.length; i++) {
				if (elem.hasClass(my_params[i])) {
					return true;
				}
			}
			elem_parent = elem.parent();
			for (var i = 0; i < my_params.length; i++) {
				if (elem_parent.hasClass(my_params[i])) {
					return true;
				}
			}
			return false;
		},
		tolerance: "pointer",
		activeClass: "ui-state-hover",
		hoverClass: "simpledroppable-hover",
		drop: function( event, ui ) {
            epfl.dispatch_event(cid, "add_dragable", {cid: ui.draggable.attr('epflid')});
		},
		
	});
	$('[epflid="'+cid+'"] > .simpledroppable-remove-button').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        epfl.dispatch_event(cid, "remove_content", {});
    });
};
epfl.SimpleDroppableComponent.inherits_from(epfl.ComponentBase);
