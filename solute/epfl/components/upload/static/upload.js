epfl.Upload = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};

epfl.Upload.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Upload.prototype, 'remove_icon', {
    get: function () {
        return this.elm.find('.epfl-upload-remove-icon');
    }
});

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
        if (obj.params.fire_change_immediately) {
            obj.send_event('change', {value: this.result});
        } else {
            obj.repeat_enqueue('change', {value: this.result});
        }
    });
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

    if (this.remove_icon.is(event.target) ) {
        this.send_event('remove_icon', {});
    } else if (this.params.handle_click) {
        this.send_event('click', {});
    }
};
