epfl.Download = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var confirm_first=params["confirm_first"];
    var confirm_message=params["confirm_message"];
    var event_name=params["event_name"];
    var event_target=params["event_target"];
	$('#' + cid + ' div button').click(function(event) {
		if (confirm_first && (!confirm(confirm_message))) {
			return;
		}
	    var request = epfl.make_component_event(event_target, event_name);
	    epfl.send(request, function(response){
            var filename;
            var result = JSON.parse(response);
            var data = result[0];
            if(result.length > 1) {
                filename = result[1];
            }
            else {
                filename = 'voucher_codes.csv';
            }
            var blob = new Blob([data], {type:'text/csv'});
            saveAs(blob, filename);
        });
	});
};
epfl.Download.inherits_from(epfl.ComponentBase);
