epfl.Select = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Select.inherits_from(epfl.ComponentBase);

epfl.Select.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);

    var obj = this;
    var selector = "#" + obj.cid +"_input";
    var enqueue_event = !obj.params.fire_change_immediately;
    var submit_form_on_enter = obj.params.submit_form_on_enter;

    $(selector).change(function(){
        epfl.FormInputBase.on_change(obj, $(this).val(), obj.cid, enqueue_event);
    });

    var keydown = function(event){
        if(event.which == 13){
            epfl.FormInputBase.event_submit_form_on_enter(obj.cid);
        }
    };
    var elm = $(selector);
    if(submit_form_on_enter){
        elm.keydown(keydown);
    }
};
