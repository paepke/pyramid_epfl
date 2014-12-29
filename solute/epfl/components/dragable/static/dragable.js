epfl.DragableComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    var tmp = $('#' + cid).draggable({
        connectToSortable: '.droppable_type_' + params.type,
        cursorAt: {top: 0, left: 0}
    });
    $('[epflid="'+cid+'"].selectable').not('.selected').click(function(event) {
    	var ev = compo.make_event("selected",{});
    	epfl.send(ev);
    });
    $('[epflid="'+cid+'"].selectable.selected').click(function(event) {
    	var ev = compo.make_event("unselected",{});
    	epfl.send(ev);
    });
    // handle title renaming
    $('[epflid="'+cid+'"].rename-inactive').bind('dblclick', function(event) {
		$(this).removeClass("rename-inactive");
		$(this).children(".inactive").removeClass("inactive");
		$(this).children(".title-rename").focus();
    });
    $('[epflid="'+cid+'"] .title-rename.inactive').bind('keyup', function(event) {
    	if ((event.type == "keyup") && (event.keyCode != 113)) { // F2
			return;
		}
		$(this).parent().removeClass("rename-inactive");
		$(this).removeClass("inactive");
    });
	$('[epflid="'+cid+'"] .title-rename').bind('keyup', function(event){
		if ((event.keyCode != 13) && (event.keyCode != 27)) {
			return;
		}
		if (event.keyCode == 27) { // ESC, undo changes
			$(this).val($(this).data("oldtitle"));
		}
		$(this).blur(); // will trigger focusout event
	});
	$('[epflid="'+cid+'"] .title-rename').bind('focusout', function(event){

		if ($(this).hasClass("inactive")) {
			return;
		}
		
		$(this).addClass("inactive");
		$(this).parent().addClass("rename-inactive");
		if ($(this).data("oldtitle") != $(this).val()) {
			$(this).data("oldtitle", $(this).val());
			var ev = compo.make_event("rename_title",{"title":$(this).val()});
			epfl.send(ev);
		}
	});
};
epfl.DragableComponent.inherits_from(epfl.ComponentBase);
