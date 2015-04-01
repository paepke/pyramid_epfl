epfl.TabsLayout = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $('#' + cid + '_tabmenu a').click(function(event) {
    	event.preventDefault();
    	if ($(this).parent().hasClass("active")) {
    		return;
    	}
    	selected_compo_cid = $(this).data('tab-compo-cid');
    	epfl.dispatch_event(cid, "toggle_tab", {"selected_compo_cid": selected_compo_cid});
	});
	window.setTimeout(function() {
		$('#'+cid).find('[role="tabpanel"]').addClass("tab-pane");
	},0);
	
};
epfl.TabsLayout.inherits_from(epfl.ComponentBase);
