epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid + "_input";
    var img_container = $('#' + cid + '_img');
    var compo = this;
    var fire_change_immediately = params["fire_change_immediately"];
    var allowed_file_types = params["allowed_file_types"];
    var show_remove_icon = params["show_remove_icon"];


    /*****************************************************/


    //Selectors
    var dropZone = $("#" + cid + " div.epfl-dropzone");

    console.log("dropZone", dropZone);

    var image = $("#" + cid + " img.epfl-upload-image");
    console.log("image", image);

    var addIcon = $("#" + cid + " p.epfl-dropzone-addicon");
    var addIconTag = $("#" + cid + " p.epfl-dropzone-addicon > i");
    var dropText = $("#" + cid + " h2");

    //EVENT Functions

    //file drop event on drop zone, prevent default for no redirection to file
    var dropEvent = function (ev) {
        console.log("drop");
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
        } else {
            //load the desktop file to show it in the image tag
            var files = ev.dataTransfer.files;
            type = "desktop";
            if (files.length) {
                url = files[0].name;
                var reader = new FileReader();
                reader.readAsDataURL(files[0]);
                reader.onload = function () {
                    image.attr('src', reader.result);
                }
            }
        }

        if (fire_change_immediately) {
            epfl.send(epfl.make_component_event(cid, "change", {
                "value": url,
                "type": type,
                "dropped_cid": droppedCid
            }));
        } else {
            epfl.dispatch_event(cid, "change", {
                "value": url,
                "type": type,
                "dropped_cid": droppedCid
            })
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
    //EVENTS
    if (params["value"] !== null) {
        addIcon.hide();
        image.show();
    } else {
        dropZone.on("dragover", dragOverEvent);
        dropZone.on("dragleave", dragLeaveEvent);
    }

    dropZone.on('drop', dropEvent);

    dropZone.click(function () {
        if (fire_change_immediately) {
            epfl.send(epfl.make_component_event(cid, "click", {}));
        } else {
            epfl.dispatch_event(cid, "click", {});
        }
    });


    /*****************************************************/


    //if a file is dragged from desktop to browser highlight the droppable area
    $(document).on("dragenter", "#" + cid, function (event) {
        $("#" + cid + " div.epfl-upload-input-zone").addClass("epfl-upload-file-over");
    });
    $(document).on("dragleave", "#" + cid, function (event) {
        $("#" + cid + " div.epfl-upload-input-zone").removeClass("epfl-upload-file-over");
    });


    //show the remove icon to remove the uploaded file
    if (show_remove_icon) {
        var remove_icon = $("#" + cid + " .epfl-upload-remove-icon");
        if (remove_icon.length) {
            var uploadImg = $("#" + cid + " img");
            $(remove_icon).click(function () {
                if (fire_change_immediately) {
                    epfl.send(epfl.make_component_event(cid, "change", {
                        "value": null,
                        "type": null,
                        "dropped_cid": null
                    }));
                } else {
                    epfl.dispatch_event(cid, "change", {
                        "value": null,
                        "type": null,
                        "dropped_cid": null
                    });
                }
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
                    alert("Unknown File Type");
                    return;
                }
                if (allowed_file_types.indexOf(filename_parts[filename_parts.length - 1]) === -1) {
                    //if filetype is not in array -> return
                    alert("Not allowed File Type");
                    return;
                }
            }
        }
        if (file.size > parseInt(params["maximum_file_size"])) {
            alert("File size to big");
            return;
        } else if (file.size > 200 * 1024 * 1024) {
            //200 MB is hard limit of upload compo
            alert("File size to big");
            return;
        }

        reader.readAsDataURL(file);
        reader.onload = function () {
            if (img_container.find('img').length !== 0) {
                img_container.find('img').attr('src', reader.result);
            }
            epfl.FormInputBase.on_change(compo, reader.result, cid, fire_change_immediately);
            if (fire_change_immediately) {
                epfl.send(epfl.make_component_event(cid, "change", {
                    "value": reader.result,
                    "type": "extern",
                    "dropped_cid": null
                }));
            } else {
                epfl.dispatch_event(cid, "change", {
                    "value": reader.result,
                    "type": "extern",
                    "dropped_cid": null
                });
            }

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
        dropZone: $("#" + cid + " div.epfl-upload-input-zone")
    });

    $(selector).blur(change).change(change);
};

epfl.Upload.inherits_from(epfl.ComponentBase);
