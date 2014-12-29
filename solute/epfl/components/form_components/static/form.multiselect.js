epfl.FormMultiSelectComponent = function (cid, params) {
    var compo = this;
    epfl.ComponentBase.call(this, cid, params);
    
	$('[epflid="'+cid+'"] > div > .multi_select_move_forward').click(function(event){
		select_index = $(this).data("selectindex");
		var ev = compo.make_event("moveforward",{"select_index":select_index});
		epfl.send(ev);
	});
	$('[epflid="'+cid+'"] > div > .multi_select_move_back').click(function(event){
		select_index = $(this).data("selectindex");
		var ev = compo.make_event("moveback",{"select_index":select_index});
		epfl.send(ev);
	});
};
epfl.FormMultiSelectComponent.inherits_from(epfl.ComponentBase);

epfl.FormMultiSelectComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};