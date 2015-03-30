epfl.BoxComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var hover_box_remove_on_close=params["hover_box_remove_on_close"];

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

    $('#' + cid + ' > .epfl_box_remove_button, #' + cid + ' > .panel-heading > .epfl_box_remove_button').click(remove_handler);
    var hover_box_remove_handler;
    if (hover_box_remove_on_close) {
    	hover_box_remove_handler = remove_handler;
    } else {
    	hover_box_remove_handler = hide_handler;
    }
    $('#' + cid + '.epfl_hover_box > div > .panel-heading > .epfl_box_remove_button, #' + cid + '.epfl_hover_box > div > .epfl_box_remove_button').click(hover_box_remove_handler);
    $('#' + cid + '.epfl_hover_box').click(function (event) {
        if (event.target.id != cid) {
            return;
        }
        hover_box_remove_handler(event);
    });

};
epfl.BoxComponent.inherits_from(epfl.ComponentBase);
