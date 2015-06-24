epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var img_container = $('#' + cid + '_img');
    var compo = this;
    var enqueue_event = !params["fire_change_immediately"];
    var allowed_file_types = params["allowed_file_types"];
    var show_remove_icon = params["show_remove_icon"];

    //if a file is dragged from desktop to browser highlight the droppable area
    $(document).on("dragenter","#" + cid,function(event) {
        $("#" + cid).addClass("epfl-upload-file-over");
    });
    $(document).on("dragleave","#" + cid,function(event) {
        $("#" + cid).removeClass("epfl-upload-file-over");
    });


    //show the remove icon to remove the uploaded file
    if (show_remove_icon) {
        var remove_icon = $("#" + cid + " .epfl-upload-remove-icon");
        if (remove_icon.length) {
            var uploadImg = $("#" + cid + " img");
            //set the icon pos to to right corner of the image
            remove_icon.css({"position": "absolute", "top": "0"});
            $(remove_icon).click(function () {
                epfl.send(epfl.make_component_event(cid, "remove_icon"));
            });
        }
    }

    var change = function (event, data) {

        var reader = new FileReader();
        var file;

        //try get first file from data
        if (data && data.files && data.files.length) {
            file = data.files[0];
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

        //check if file type is allowed
        if (allowed_file_types) {
            if (file) {
                var filename_parts = file.name.split('.');
                if (filename_parts.length === 1) {
                    //no file type found (no dot in filename) -> return
                    return;
                }
                if (allowed_file_types.indexOf(filename_parts[filename_parts.length - 1]) === -1) {
                    //if filetype is not in array -> return
                    return;
                }
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
            change(evt, data);
        },
        dropZone: $("#" + cid)
    });

    $(selector).blur(change).change(change);
};

epfl.Upload.inherits_from(epfl.ComponentBase);
