epfl.MultiSelectComponent = function (cid, params) {
    if (params.scroll_position > 0) {
    	$('[epflid="'+cid+'"] > .list-group').scrollTop(params.scroll_position);
    }
    epfl.ComponentBase.call(this, cid, params);
    $('[epflid="'+cid+'"] > .list-group > .list-group-item.multiselect-selectable').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        child_cid = $(this).children().first().attr("epflid");
    	epfl.dispatch_event(cid, "selected", {child_cid: child_cid});
    });
    $('[epflid="'+cid+'"] > .list-group > .list-group-item.multiselect-selected').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        child_cid = $(this).children().first().attr("epflid");
    	epfl.dispatch_event(cid, "unselected", {child_cid: child_cid});
    });
    // Remember scroll position
    $('[epflid="'+cid+'"] > .list-group').scroll(function() {
    	clearTimeout($.data(this, 'multiselect_scrolltimer'));
    	$.data(this, 'multiselect_scrolltimer', setTimeout(function() { // detect scroll stop
        	scrolltop = $('[epflid="'+cid+'"] > .list-group').scrollTop();
    		epfl.dispatch_event(cid, "scrolled", {scroll_position: scrolltop});
    	}, 250));
	});
	// Search
	$('[epflid="'+cid+'"] > .multiselect-search-input').keydown(function(event) {
    	if (event.keyCode == 13) {
    		search_string = $(this).val();
    		epfl.dispatch_event(cid, "search", {search_string: search_string});
	    }
	})
};
epfl.MultiSelectComponent.inherits_from(epfl.ComponentBase);
