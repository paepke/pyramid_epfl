epfl.TextInput = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var max_length = params["max_length"];
    var show_count = params["show_count"];
    var typeahead = params["typeahead"];
    var type_func = params["type_func"];
    var date = params["date"];
    var source = params["source"];

    if(typeahead) {
        var type_function = function(query, process){
            var get_source = function(epfl_event){
                epfl.send(epfl_event, function(response){
                    if(response && response !== "") {
                        response = $.parseJSON(response);
                        var i = 0, result_set = [];
                        for (i; i < response.length; i++) {
                            result_set.push({'id': response[i][0], 'name': response[i][1]});
                        }
                        process(result_set);
                    }
                });
            };

            var event = epfl.make_component_event(cid, type_func, {"query": query, "compo": cid}, cid + '_typeahead');
            return get_source(event);
        };
        $(selector).typeahead({source: type_function,
                               items: 'all',
                               autoSelect: false});
    }
    if(date){
        $(selector).datetimepicker({
            format:'d.m.Y H:i',
            closeOnTimeSelect: true,
            lang: 'de'
        });
    }
    var change = function (event) {
        epfl.FormInputBase.on_change(compo, $(selector).val(), cid, enqueue_event);
        if(show_count && max_length){
            $(selector + '_count').text($(selector).val().length);
        }
    };

    $(selector).blur(change).change(change).keydown(change);
};

epfl.TextInput.inherits_from(epfl.ComponentBase);
