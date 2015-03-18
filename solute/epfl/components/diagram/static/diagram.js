epfl.DiagramComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $('#'+cid).highcharts(
        params
    );
    // handle changes in series visibility
    $('#'+cid).find('.highcharts-legend-item').click(function(event) {
    	var my_chart = $('#'+cid).highcharts();
    	series_visibility = [];
        for (var i = 0; i < my_chart.series.length; i++) {
		    series = my_chart.series[i];
		    series_json = { "name": series.name };
		    if (series.visible == false) {
		    	series_json["visible"] = false;
		    }
		    series_visibility.push(series_json);
		}
		epfl.dispatch_event(cid, "visibilityChange", {"series_visibility":series_visibility});
    });   
};

epfl.DiagramComponent.inherits_from(epfl.ComponentBase);
