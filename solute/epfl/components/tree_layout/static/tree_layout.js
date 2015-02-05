epfl.TreeLayoutComponent = function(cid, params) {

	var show_context_menu_on_hover_only = params["show_context_menu_on_hover_only"];
    epfl.ComponentBase.call(this, cid, params);
	$('[epflid=' + cid + '] > .epfl-tree-label.expanded')
	    .click(function () {
	    	epfl.dispatch_event(cid, "hide", {});
	    });
	
	$('[epflid=' + cid + '] > .epfl-tree-label.collapsed')
	    .click(function () {
	    	epfl.dispatch_event(cid, "show", {});
	    });
	if (show_context_menu_on_hover_only) {
		$('[epflid=' + cid + '] > .epfl-tree-label').mouseenter(function() {
			$(this).parent().parent().children('.epfl-tree-context-menu').hide();
			$(this).children('.epfl-tree-context-menu').show();
		})
		.mouseleave(function() {
			$(this).children('.epfl-tree-context-menu').hide();
		});
	
	}
};
epfl.TreeLayoutComponent.inherits_from(epfl.ComponentBase);
