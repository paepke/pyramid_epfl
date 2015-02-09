epfl.BoxComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    hover_box_remove_on_close=params["hover_box_remove_on_close"];

    function remove_handler(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	epfl.dispatch_event(cid, "removed", {});
    }
    function hide_handler(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	epfl.dispatch_event(cid, "hide", {});
    }

    $('[epflid="'+cid+'"] > .epfl_box_remove_button, [epflid="'+cid+'"] > .panel-heading > .epfl_box_remove_button').click(remove_handler);
    if (hover_box_remove_on_close) {
    	hover_box_remove_handler = remove_handler;
    } else {
    	hover_box_remove_handler = hide_handler;
    }
    $('[epflid="'+cid+'"].epfl_hover_box > div > .panel-heading > .epfl_box_remove_button, [epflid="'+cid+'"].epfl_hover_box > div > .epfl_box_remove_button').click(hover_box_remove_handler);
    $('[epflid="'+cid+'"].epfl_hover_box').click(function (event) {
        if (!event.target.getAttribute('epflid') || event.target.getAttribute('epflid') != cid) {
            return;
        }
        hover_box_remove_handler(event);
    });

};
epfl.BoxComponent.inherits_from(epfl.ComponentBase);
