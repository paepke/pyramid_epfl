epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var img_container = $('#' + cid + '_img');
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    var change = function (event) {
        var reader = new FileReader();
        var file = $(selector)[0].files[0];
        if (!file){
            try {
                // Check if file was added with paste (only Chrome)
                items = event.clipboardData.items;
                var i = 0;
                for(; i < items.length; i++){
                    file = items[i].getAsFile();
                    if(file){
                        // It's a file that was pasted
                        break;
                    }
                }
            }
            catch (e){
                return;
            }
        }
        reader.readAsDataURL(file);
        reader.onload = function(){
            if (img_container.find('img').length != 0) {
                img_container.find('img').attr('src', reader.result);
            }
            epfl.FormInputBase.on_change(compo, reader.result, cid, enqueue_event);
        }
    };

    $(selector).fileupload({
        add: function(evt, data){
            try {
                evt = evt.delegatedEvent.originalEvent;
            }
            catch (e){
                //ignore errors and just return
                return;
            }
            change(evt);
        }
    });

    $(selector).blur(change).change(change);
};

epfl.Upload.inherits_from(epfl.ComponentBase);
