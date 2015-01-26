epfl.InputComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
	var compo = this;
    var selector = "#" + cid;
	var type = $(selector).closest("div").attr('epfl-type');
	
	if (type == "defaultinput" || type == "textarea" || type == "select") {
	    $(selector).change(function () {
	        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: $(selector).val()}), cid);
	    });
	
	    provide_typeahead = $(selector).data("provide");
	    if (provide_typeahead == "typeahead") {
	        $(selector).typeahead({
	            source: function (query, process) {
	            	res = epfl.send(compo.make_event("typeahead",{"query":query}));
	            	// todo: results have to be returned from server
	                return process(['Amsterdam', 'Washington', 'Sydney', 'Beijing', 'Cairo']);
	            }
	        });
	    }
	
	} else if (type == "checkbox") {
	    $(selector).attr('checked', $(selector).val() == 'True');
	    $(selector).change(function () {
	        var val = val = $(this).is(':checked');
	        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	    });
	
	} else if (type == "toggle") {
	    $(selector).attr('checked', $(selector).val() == 'True');
	    $(selector).bootstrapSwitch('state');
	    $(selector).on('switchChange.bootstrapSwitch', function (event, state) {
	        var val = $(this).closest("div").parent().hasClass("bootstrap-switch-on");
	        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	    });
	
	} else if (type == "radiobuttongroup") {
	    selector = "input[type=radio][name="+cid+"]";
	    $(selector).change(function () {
	        var val = $(this).val();
	        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	    });
	
	} else if (type == "buttonsetgroup") {
	    selector = "input[type=radio][name="+cid+"]";
	    $(selector).change(function () {
	        var val = $(this).val();
	        var parent = $(this).parent().parent();
	        $(parent).find("label").removeClass("active");
	        $(this).parent().addClass("active");
	        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value: val}), cid);
	    });
	
	}
	if (params["submit_form_on_enter"]) {
		$(selector).bind('keyup', function(event){
			if (event.keyCode == 13) {
				//res = epfl.send(compo.make_event("submit",{}));
				var request = epfl.make_component_event(cid, "submit", {}); // blubbles up to form
    			epfl.send(request);
			}
		});
	}
	 
}; 
epfl.InputComponent.inherits_from(epfl.ComponentBase);

