epfl.DragableComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    var tmp = $('#' + cid).draggable({
        connectToSortable: '.droppable_type_' + params.type,
        cursorAt: {top: 0, left: 0}
    });
    $('[epflid="'+cid+'"].selectable').click(function(event) {
    	var ev = compo.make_event("selected",{});
    	epfl.send(ev);
    });
};
epfl.DragableComponent.inherits_from(epfl.ComponentBase);
