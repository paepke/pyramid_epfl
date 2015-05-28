epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var img_container = $('#' + cid + '_img');
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];

    var change = function (event) {
        var reader = new FileReader();
        var file;
        // First try if the event itself has a reference to the uploaded file
        if (event.target && event.target.files) {
            file = event.target.files[0];
        }
        if (!file) {
            try {
                // Check if file was added with paste (only Chrome)
                items = event.clipboardData.items;
                var i = 0;
                for (; i < items.length; i++) {
                    file = items[i].getAsFile();
                    if (file) {
                        // It's a file that was pasted
                        break;
                    }
                }
            }
            catch (e) {
                // Change was triggered but there is no file, not selected by dialog, nor pasted via keyboard-commands,
                // but it is possible that items contains a single text string which would result in an error when
                // items[i].getAsFile() is executed on that string.
                return;
            }
        }
        reader.readAsDataURL(file);
        reader.onload = function () {
            if (img_container.find('img').length !== 0) {
                img_container.find('img').attr('src', reader.result);
            }
            epfl.FormInputBase.on_change(compo, reader.result, cid, enqueue_event);
        }
    };

    $(selector).fileupload({
        add: function (evt, data) {
            try {
                evt = evt.delegatedEvent.originalEvent;
            }
            catch (e) {
                //ignore errors and just return
                return;
            }
            change(evt);
        }
    });

    $(selector).blur(change).change(change);
};

epfl.Upload.inherits_from(epfl.ComponentBase);
