epfl.DropdownComponent = function (cid, params) {
    $('[epflid="'+cid+'"] > .dropdown-toggle').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        $(this).dropdown('toggle');
	});
	$('[epflid="'+cid+'"] > ul > li > .epfl_dropdown_menuitem').click(function(event) {
		event.stopImmediatePropagation();
	    event.preventDefault();
	    menu_key = $(this).data("menu-key");
	    $(this).parent().parent().prev().dropdown('toggle');
	    epfl.dispatch_event(cid, "item_selected", {key: menu_key});
	});
};
epfl.DropdownComponent.inherits_from(epfl.ComponentBase);
