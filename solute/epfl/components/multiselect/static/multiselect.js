epfl.MultiSelectComponent = function (cid, params) {
    if (params.scroll_position > 0) {
    	$('[epflid="'+cid+'"] > .list-group').scrollTop(params.scroll_position);
    }
    var multiselect_double_click_delay = 400;
    var multiselect_clicks = 0;
    var multiselect_double_click_timer = null;
    epfl.ComponentBase.call(this, cid, params);
    $('[epflid="'+cid+'"] > .list-group > .list-group-item.multiselect-selectable').click(function(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
        multiselect_clicks++;  //count clicks
        my_elem = $(this);
        if(multiselect_clicks === 1) {
            multiselect_double_click_timer = setTimeout(function() {
                //perform single-click action
            	if (my_elem.hasClass("selected")) {
					child_cid = my_elem.children().first().attr("epflid");
					epfl.dispatch_event(cid, "unselected", {child_cid: child_cid});
				} else {
					child_cid = my_elem.children().first().attr("epflid");
					epfl.dispatch_event(cid, "selected", {child_cid: child_cid});
				}
                
                multiselect_clicks = 0;             //after action performed, reset counter
            }, multiselect_double_click_delay);
        } else {
            clearTimeout(multiselect_double_click_timer);    //prevent single-click action
            
            //perform double-click action
        	child_cid = my_elem.children().first().attr("epflid");
			epfl.dispatch_event(cid, "double_click", {child_cid: child_cid});
            multiselect_clicks = 0;             //after action performed, reset counter
        }
        
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
