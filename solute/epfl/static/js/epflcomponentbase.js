epfl.ComponentBase = function (cid, params) {
    this.cid = cid;
    this.params = params;
};

Object.defineProperty(epfl.ComponentBase.prototype, 'elm', {
    get: function () {
        return $("[epflid='" + this.cid + "']");
    }
});

epfl.ComponentBase.prototype.make_event = function (event_name, params) {
    return epfl.make_component_event(this.cid, event_name, params);
};

epfl.ComponentBase.prototype.send_event = function (event_name, params, callback) {
    epfl.send(epfl.make_component_event(this.cid, event_name, params), callback);
};

epfl.ComponentBase.prototype.closest_cid = function (element) {
    var containing_elm = $(element);
    var cid = containing_elm.attr('epflid');
    if (!cid) {
        cid = containing_elm.parent().attr('epflid');
    }
    if (!cid) {
        cid = containing_elm.parentsUntil('[epflid]').parent().attr('epflid');
    }
    return cid;
};

/* Lifecycle methods */

epfl.ComponentBase.prototype.after_response = function (data) { // Extend me!
    if (this.params && this.params.lifecycle_handle_click) {
        var obj = this;
        this.elm.click(function (event) {
            obj.handle_click(event);
        });
    }
};

epfl.ComponentBase.prototype.before_response = function (data) {
}; // Overwrite me!

epfl.ComponentBase.prototype.before_request = function () {
}; // Overwrite me!

epfl.ComponentBase.prototype.destroy = function () {
}; // Overwrite me!

/* Predefined handle functions */

epfl.ComponentBase.prototype.handle_local_click = function (event) {
}; // Overwrite me!

epfl.ComponentBase.prototype.handle_click = function (event) { // Extend me!
    var cid = this.closest_cid(event.target);
    if (cid == this.cid) {
        this.handle_local_click(event);
    }
};
