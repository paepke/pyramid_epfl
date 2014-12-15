epfl.DragableComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var tmp = $('#' + cid).draggable({
        connectToSortable: '.droppable_type_' + params.type,
        cursorAt: {top: 0, left: 0}
    });
};
epfl.DragableComponent.inherits_from(epfl.ComponentBase);
