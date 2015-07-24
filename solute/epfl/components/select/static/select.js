epfl.Select = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid +"_input";
    var compo = this;
    var enqueue_event = !params.fire_change_immediately;
    var submit_form_on_enter = params.submit_form_on_enter;

    $(selector).change(function(){
        epfl.FormInputBase.on_change(compo, $(this).val(), cid, enqueue_event);
    });

    var keydown = function(event){
        if(event.which == 13){
            epfl.FormInputBase.event_submit_form_on_enter(cid);
        }
    };
    var elm = $(selector);
    if(submit_form_on_enter){
        elm.keydown(keydown);
    }

};

epfl.Select.inherits_from(epfl.ComponentBase);
