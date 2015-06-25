epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var reader = new FileReader();
    //params
    var fire_change_immediately = params["fire_change_immediately"];
    var allowed_file_types = params["allowed_file_types"];
    var show_remove_icon = params["show_remove_icon"];

    //jquery selectors
    var selector = "#" + cid;
    var inputSelector = selector + "_input";
    var img_container = $(selector + '_img');
    var dropZone = $(selector + " div.epfl-dropzone");
    var image = $(selector + " img.epfl-upload-image");
    var addIcon = $(selector + " p.epfl-dropzone-addicon");
    var dropText = $(selector + " h2");

    /**************************************************************************
     Helper Functions
     *************************************************************************/
    var endsWith = function (str, suffix) {
        // Check if the given string ends with the given suffix.
        // As endsWith will (should) be implemented with ES6 this might get obsolete
        return str.indexOf(suffix, str.length - suffix.length) !== -1;
    };

    var validateFile = function (file) {
        var type_is_allowed = false;
        var i = 0;
        //check if file type is allowed
        if (allowed_file_types) {
            if (file) {
                for (; i < allowed_file_types.length; i++){
                    if(endsWith(file.name, allowed_file_types[i])){
                        type_is_allowed = true;
                    }
                }
                if (!type_is_allowed){
                    alert("Unknown File Type");
                    return false;
                }
            }
        }
        if (file.size > parseInt(params["maximum_file_size"])) {
            alert("File size to big");
            return false;
        } else if (file.size > 200 * 1024 * 1024) {
            //200 MB is hard limit of upload compo
            alert("File size to big");
            return false;
        }
        return true;
    };
    //Send the change event
    var sendChange = function (value, type, droppedCid) {
        if (fire_change_immediately) {
            epfl.send(epfl.make_component_event(cid, "change", {
                "value": value,
                "type": type,
                "dropped_cid": droppedCid
            }));
        } else {
            epfl.dispatch_event(cid, "change", {
                "value": value,
                "type": type,
                "dropped_cid": droppedCid
            })
        }
    };

    // called when the reader is finished sets the image in the container and fires change event
    var readerFinishedLoading = function () {
        if (img_container.find('img').length !== 0) {
            img_container.find('img').attr('src', reader.result);
        }
        sendChange(reader.result, "desktop", null)
    };

    /**************************************************************************
     Event Functions
     *************************************************************************/

    //file drop event on drop zone, prevent default for no redirection to file
    var dropEvent = function (ev) {
        ev.preventDefault();

        //show the image and hide the plus icon
        addIcon.hide();
        image.show();
        dropText.hide();
        dropZone.css({"border-color": "#D7D7D7"});

        //get the html tag of the dragged image
        var dataTransfer = $(ev.dataTransfer.getData('text/html'));

        //extract src and check if the image is from a epfl compo
        var url = dataTransfer.attr("src");
        var droppedCid = dataTransfer.data("cid") || null;
        var isEpflUpload = dataTransfer.hasClass("epfl-upload-image");
        var isEpflImage = dataTransfer.hasClass("epfl-img-component-image");


        var type = null;
        //if the image has a url(src) its source is from the browser else the source is desktop
        if (url) {
            type = "extern";
            if (isEpflUpload) {
                type = "epfl_upload_image";
            }
            if (isEpflImage) {
                type = "epfl_image";
            }
            image.attr('src', url);
            sendChange(url, type, droppedCid);
        } else {
            //load the desktop file to show it in the image tag
            var files = ev.dataTransfer.files;
            type = "desktop";
            if (files.length) {

                if (!validateFile(files[0])) {
                    return;
                }
                reader.readAsDataURL(files[0]);
                reader.onload = readerFinishedLoading;
            }
        }
    };

    //drag a file over, prevent default for no redirection
    var dragOverEvent = function (ev) {
        ev.preventDefault();
        addIcon.hide();
        dropText.show();
        dropZone.css({"border-color": "#1BB7A0"});
    };

    //drag file out event
    var dragLeaveEvent = function (ev) {
        ev.preventDefault();
        addIcon.show();
        dropText.hide();
        dropZone.css({"border-color": "#D7D7D7"});
    };

    //fired when the fileinput changes
    var fileInputChange = function (event, data) {
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

        if (!validateFile(file)) {
            return;
        }

        reader.readAsDataURL(file);
        reader.onload = readerFinishedLoading;
    };

    var dropZoneClick = function () {
        if (fire_change_immediately) {
            epfl.send(epfl.make_component_event(cid, "click", {}));
        } else {
            epfl.dispatch_event(cid, "click", {});
        }
    };

    //Add File Event from file input
    var fileInputAdd = function (evt, data) {
        try {
            evt = evt.delegatedEvent.originalEvent;
        }
        catch (e) {
            //ignore errors and just return
            return;
        }
        fileInputChange(evt, data);
    };

    /**************************************************************************
     Event Handler
     *************************************************************************/

    //Drop Zone Events
    dropZone.on("dragover", dragOverEvent);
    dropZone.on("dragleave", dragLeaveEvent);
    dropZone.on('drop', dropEvent);
    dropZone.click(dropZoneClick);

    //File Input Events
    $(inputSelector).fileupload({
        add: fileInputAdd,
        dropZone: $("#" + cid + " div.epfl-upload-input-zone")
    });

    //Remove Icon Event
    if (show_remove_icon) {
        var remove_icon = $("#" + cid + " .epfl-upload-remove-icon");
        if (remove_icon.length) {
            $(remove_icon).click(function () {
                sendChange(null, null, null);
            });
        }
    }

};

epfl.Upload.inherits_from(epfl.ComponentBase);
