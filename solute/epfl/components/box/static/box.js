epfl.BoxComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    function remove_handler(event) {
    	event.stopImmediatePropagation();
        event.preventDefault();
    	epfl.dispatch_event(cid, "removed", {});
    }

    $('[epflid="'+cid+'"] > .epfl_box_remove_button').click(remove_handler);
    $('[epflid="'+cid+'"].epfl_hover_box > div > .epfl_box_remove_button').click(remove_handler);
    $('[epflid="'+cid+'"].epfl_hover_box').click(function (event) {
        if (!event.target.getAttribute('epflid') || event.target.getAttribute('epflid') != cid) {
            return;
        }
        remove_handler(event);
    });

};
epfl.BoxComponent.inherits_from(epfl.ComponentBase);
