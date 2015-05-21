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
    /* Calculates the cid of the closest epfl component containing the given element. */

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

epfl.ComponentBase.prototype.after_response = function (data) {
    /* Called after a server response has been handled. On a full page request that is after all init steps are done,
     * during an ajax request this will be called after the response javascript has been executed or sent to the
     * callback. */
    if (this.params && this.params.extras_handle_click) {
        var obj = this;
        this.elm.click(function (event) {
            obj.handle_click(event);
        });
    }
};

epfl.ComponentBase.prototype.before_response = function (data) {
    /* Called before an ajax response is executed or sent to its callback, but after it was received from the server. */
};

epfl.ComponentBase.prototype.before_request = function () {
    /* Called before the actual ajax request is sent to the server. The queue may still be modified at this time. */
};

epfl.ComponentBase.prototype.destroy = function () {
}; // Overwrite me!

/* Predefined handle functions */

epfl.ComponentBase.prototype.handle_local_click = function (event) {
    /* Executed on click events if extras_handle_click is set to true. Local clicks are all clicks that have been
     * directly on this components html element or on any html element that has no more direct containing component. */
};

epfl.ComponentBase.prototype.handle_click = function (event) {
    /* Executed on click events if extras_handle_click is set to true. */
    var cid = this.closest_cid(event.target);
    if (cid == this.cid) {
        this.handle_local_click(event);
    }
};
