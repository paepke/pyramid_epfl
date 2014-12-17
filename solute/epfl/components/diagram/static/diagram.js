epfl.DiagramComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    $('#' + cid).highcharts(
        params
    );
    // handle changes in series visibility
    $('#' + cid + ' .highcharts-legend-item').click(function(event) {
    	var my_chart = $('#' + cid).highcharts();
    	series_visibility = [];
        for (var i = 0; i < my_chart.series.length; i++) {
		    series = my_chart.series[i];
		    series_json = { "name": series.name };
		    if (series.visible == false) {
		    	series_json["visible"] = false;
		    }
		    series_visibility.push(series_json);
		}
		var ev = compo.make_event("visibilityChange",{"series_visibility":series_visibility});
        epfl.send(ev); 
    });
    

};
epfl.DiagramComponent.inherits_from(epfl.ComponentBase);

epfl.DiagramComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};


