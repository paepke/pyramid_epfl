epfl.DragableComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var tmp = $('#' + cid).draggable({
        connectToSortable: '.droppable_type_' + params.type,
        cursorAt: {top: 0, left: 0},
        delay: 500,
        zIndex: 9999
    });
    $('#' + cid+'.selectable').not('.selected').click(function(event) {
    	epfl.dispatch_event(cid, "selected", {});
    });
    $('#' + cid+'.selectable.selected').click(function(event) {
    	epfl.dispatch_event(cid, "unselected", {});
    });
    // handle title renaming
    $('#' + cid+'.rename-inactive').bind('dblclick', function(event) {
		$(this).removeClass("rename-inactive");
		$(this).children(".inactive").removeClass("inactive");
		$(this).children(".title-rename").focus();
    });
    $('#' + cid+' .title-rename.inactive').bind('keyup', function(event) {
    	if ((event.type == "keyup") && (event.keyCode != 113)) { // F2
			return;
		}
		$(this).parent().removeClass("rename-inactive");
		$(this).removeClass("inactive");
    });
	$('#' + cid+' .title-rename').bind('keyup', function(event){
		if ((event.keyCode != 13) && (event.keyCode != 27)) {
			return;
		}
		if (event.keyCode == 27) { // ESC, undo changes
			$(this).val($(this).data("oldtitle"));
		}
		$(this).blur(); // will trigger focusout event
	});
	$('#' + cid+' .title-rename').bind('focusout', function(event){

		if ($(this).hasClass("inactive")) {
			return;
		}
		
		$(this).addClass("inactive");
		$(this).parent().addClass("rename-inactive");
		if ($(this).data("oldtitle") != $(this).val()) {
			$(this).data("oldtitle", $(this).val());
			epfl.dispatch_event(cid, "rename_title", {"title":$(this).val()});
		}
	});
};
epfl.DragableComponent.inherits_from(epfl.ComponentBase);
