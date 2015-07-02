epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Upload.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Upload.prototype, 'remove_icon', {
    get: function () {
        return this.elm.find('.epfl-upload-remove-icon');
    }
});

epfl.Upload.prototype.after_response = function (data) {
    epfl.ComponentBase.prototype.after_response.call(this, data);
    var obj = this;
    if (obj.params['show_file_upload_input']) {
        obj.elm.find("input").fileupload({
            add: obj.file_input_add.bind(obj),
            dropZone: obj.elm.find("div.epfl-upload-input-zone")
        });
    }
};

epfl.Upload.prototype.file_input_add = function (evt, data) {
    var obj = this;
    try {
        evt = evt.delegatedEvent.originalEvent;
    }
    catch (e) {
        //ignore errors and just return
        return;
    }

    var files;
    //try get first file from data
    if (data && data.files && data.files.length) {
        files = data.files;
    }

    if (!files) {
        files = [];
        try {
            // Check if file was added with paste (only Chrome)
            items = event.clipboardData.items;
            var i = 0;
            for (; i < items.length; i++) {
                var file = items[i].getAsFile();
                if (file) {
                    // It's a file that was pasted
                    files.push(file);
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

    if (files) {
        obj.handle_drop_file(files, evt);
    }
};

epfl.Upload.prototype.validate_file = function (file) {
    var type_is_allowed = false;
    var i = 0;
    //check if file type is allowed
    if (this.params.allowed_file_types) {
        if (file) {
            for (; i < this.params.allowed_file_types.length; i++) {
                if (file.name.endsWith(this.params.allowed_file_types[i])) {
                    type_is_allowed = true;
                }
            }
            if (!type_is_allowed) {
                alert("Unknown File Type");
                return false;
            }
        }
    }
    if (file.size > parseInt(this.params.maximum_file_size)) {
        alert("File size to big");
        return false;
    } else if (file.size > 200 * 1024 * 1024) {
        //200 MB is hard limit of upload compo
        alert("File size to big");
        return false;
    }
    return true;
};

epfl.Upload.prototype.read_file = function (file, callback) {
    if (!this.validate_file(file)) {
        return false;
    }
    var reader = new FileReader();
    reader.onload = callback;
    reader.readAsDataURL(file);

    return true;
};

epfl.Upload.prototype.handle_drop_file = function (files, event) {
    var obj = this;

    // Currently only single files supported, although that's really only a question of implementing a backend.
    this.read_file(files[0], function () {
        obj.upload_file(this, files[0])
    });
};

epfl.Upload.prototype.upload_file = function (reader, file) {
    var obj = this;
    if (obj.params.store_async) {
        if(!file.name){
            file.name = "external"
        }
        obj.send_async_event('store', {data: reader.result, file_name: file.name}, function (data) {
            obj.handle_drop_url(data);
        });
    } else if (obj.params.fire_change_immediately) {
        obj.send_event('change', {value: reader.result});
    } else {
        obj.repeat_enqueue('change', {value: reader.result});
    }
};

epfl.Upload.prototype.handle_drop_url = function (url, event) {
    if (this.params.fire_change_immediately) {
        this.send_event('change', {value: url});
    } else {
        this.repeat_enqueue('change', {value: url});
    }
};

epfl.Upload.prototype.handle_click = function (event) {
    epfl.ComponentBase.prototype.handle_click.call(this, event);

    if (this.remove_icon.is(event.target)) {
        this.send_event('remove_icon', {});
    } else if (this.params.handle_click) {
        this.send_event('click', {});
    }
};