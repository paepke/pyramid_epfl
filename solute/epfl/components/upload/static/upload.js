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
    $(this.elm).find(".epfl-dropzone").hide();
    $(this.elm).append("<div class='text-center text-primary'><i class='fa fa-cog fa-5x fa-spin'></i></div>");
    this.read_file(files[0], function () {
        obj.upload_file(this, files[0])
    });
};

epfl.Upload.prototype.upload_file = function (reader, file) {
    var obj = this;
    if (obj.params.store_async) {
        if (!file.name) {
            file.name = "external"
        }

        obj.send_async_event('store', {data: reader.result, file_name: file.name}, function (data) {
            obj.handle_drop_url(data);
        });
    } else {
        obj.change(reader.result);
    }
};

epfl.Upload.prototype.handle_drop_url = function (url, event) {
    this.change(url);
};

epfl.Upload.prototype.change = function (value) {
    var enqueue_event = true;
    if (this.params.fire_change_immediately) {
        enqueue_event = false;
    }
    var parent_form = this.elm.closest('.epfl-form');
    if (parent_form.length == 1) {
        var is_dirty = parent_form.data('dirty');
        if (is_dirty == '0') {
            parent_form.data('dirty', '1');
            // first change to the form. always send event immediately so that
            // the serve can handle is_dirty change
            enqueue_event = false;

            this.repeat_enqueue('set_dirty', {}, this.cid + "_set_dirty");
        }
    }
    if (enqueue_event) {
        this.repeat_enqueue('change', {value: value}, this.cid + "_change");
    } else {
        this.send_event('change', {value: value});
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
