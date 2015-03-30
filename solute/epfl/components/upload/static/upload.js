epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    var change = function (event) {
        var reader = new FileReader();
        var file = $(selector)[0].files[0];
        if (!file){
            return;
        }
        reader.readAsDataURL(file);
        reader.onload = function(){
            epfl.FormInputBase.on_change(compo, reader.result, cid, enqueue_event);
        }
    };

    $(selector).blur(change).change(change);
};

epfl.Upload.inherits_from(epfl.ComponentBase);
