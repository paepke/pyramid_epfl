epfl.TabsComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    $('#' + cid + '_tabmenu a').click(function () {
    	selected_compo_cid = $(this).data('tab-compo-cid');
  		var ev = compo.make_event("toggleTab",{"selected_compo_cid":selected_compo_cid});
        epfl.send(ev); 
	});
	window.setTimeout(function() {
		$('[epflid="'+cid+'"]').find('[role="tabpanel"]').addClass("tab-pane");
	},0);
	
};
epfl.TabsComponent.inherits_from(epfl.ComponentBase);

epfl.TabsComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};


