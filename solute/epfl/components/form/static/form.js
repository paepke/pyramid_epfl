epfl.FormComponent = function (cid, params) {
	$('#'+cid).submit(function(event) {
	    event.preventDefault();
	    epfl.dispatch_event(cid, "submit", {});
	});
	var set_dirty = function() {
			is_dirty = $('#'+cid).data('dirty');
			if (is_dirty == '0') {
				$('#'+cid).data('dirty', '1');
				return true;
			}
			return false;
	        
	};
	epfl.set_component_info(cid, 'before_send_event', 'set_dirty', set_dirty);
};
epfl.FormComponent.inherits_from(epfl.ComponentBase);