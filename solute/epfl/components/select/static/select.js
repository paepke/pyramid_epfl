epfl.Select = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid +"_input";
    var compo = this;
    console.log(cid + " params[fire_change_immediately]: " + params["fire_change_immediately"]);
    var enqueue_event = !params["fire_change_immediately"]; 

    $(selector).change(function(){
        epfl.FormInputBase.on_change(compo, $(this).val(), cid, enqueue_event);
    });

};

epfl.Select.inherits_from(epfl.ComponentBase);
