epfl.MultiSelectComponent = function (cid, params) {
    var compo = this;
    if (params.scroll_position > 0) {
    	$('[epflid="'+cid+'"] > .list-group').scrollTop(params.scroll_position);
    }
    epfl.ComponentBase.call(this, cid, params);
    $('[epflid="'+cid+'"] > .list-group > .list-group-item.multiselect-selectable').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        child_cid = $(this).children().first().attr("epflid");
    	var ev = compo.make_event("selected",{child_cid: child_cid});
    	epfl.send(ev);
    });
    $('[epflid="'+cid+'"] > .list-group > .list-group-item.multiselect-selected').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        child_cid = $(this).children().first().attr("epflid");
    	var ev = compo.make_event("unselected",{child_cid: child_cid});
    	epfl.send(ev);
    });
    // Remember scroll position
    $('[epflid="'+cid+'"] > .list-group').scroll(function() {
    	clearTimeout($.data(this, 'multiselect_scrolltimer'));
    	$.data(this, 'multiselect_scrolltimer', setTimeout(function() { // detect scroll stop
        	scrolltop = $('[epflid="'+cid+'"] > .list-group').scrollTop();
    		var ev = compo.make_event("scrolled",{scroll_position: scrolltop});
    		epfl.send(ev);
    	}, 250));
	});
	// Search
	$('[epflid="'+cid+'"] > .multiselect-search-input').keydown(function(event) {
    	if (event.keyCode == 13) {
    		search_string = $(this).val();
        	var ev = compo.make_event("search",{search_string: search_string});
    		epfl.send(ev);
	    }
	})
};
epfl.MultiSelectComponent.inherits_from(epfl.ComponentBase);
