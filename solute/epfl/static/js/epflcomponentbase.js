$.event.props.push('dataTransfer');

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
    var obj = this;
    if (this.params && this.params.extras_handle_click) {
        obj.elm.click(function (event) {
            obj.handle_click(event);
        });
    }

    if (this.params && this.params.extras_handle_drop) {
        obj.elm
            .addClass('root_drop')
            .on('dragover', function (event) {
                event.preventDefault();
                clearTimeout(obj.leave_timeout);
                var current_target = obj.closest_cid(event.originalEvent.target);
                if (obj.drop_target == current_target) {
                    return;
                }
                obj.handle_drop_leave(event);
                obj.drop_target = current_target;
                obj.send_event('drop_accepts', {
                    cid: obj.drop_target
                }, function (data) {
                    if (data === true) {
                        obj.handle_drop_accepts(event);
                    }
                });
                return true;
            })
            .on('dragleave', function (event) {
                obj.leave_timeout = setTimeout(function () {
                    obj.handle_drop_leave(event);
                }, 0);
            })
            .on('drop', function(event) {
                event.preventDefault();
                obj.handle_drop(event);
            });
    }

    if (this.params && this.params.extras_handle_drag) {
        obj.elm
            .attr('draggable', true)
            .on('dragstart', function (event) {
                var dT = event.dataTransfer;
                dT.setData('text', obj.cid);
                dT.dropEffect = 'move';
                obj.handle_drag_start(event);
            });
    }

    if (this.params && this.params.extras_handle_keyup) {
        obj.elm.keyup(function (event) {
            obj.handle_keyup(event);
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

epfl.ComponentBase.prototype.handle_drop_accepts = function (event) {
    /* Executed on EPFL drag events if extras_handle_drop is set to true. Overwrite to provide behaviour when an element
       is hovered over here. */
    if (!this.drop_target) {
        return;
    }
    var target = epfl.components[this.drop_target];
    if (!target) {
        return;
    }
    target = target.elm;
    target.addClass('active_drop');
};

epfl.ComponentBase.prototype.handle_drop_leave = function (event) {
    /* Executed on EPFL drag events if extras_handle_drop is set to true. */
    if (!this.drop_target) {
        return;
    }
    var target = epfl.components[this.drop_target];
    if (!target) {
        return;
    }
    target = target.elm;
    target.removeClass('active_drop');
    delete this.drop_target;
};

epfl.ComponentBase.prototype.handle_drop = function (event) {
    /* Executed on EPFL drag events if extras_handle_drag is set to true. */
    epfl.components[event.dataTransfer.getData('text')].send_event('drag_stop', {
        cid: this.cid,
        over_cid: this.drop_target
    });
    this.handle_drop_leave();
};

epfl.ComponentBase.prototype.handle_drag_start = function (event, dd) {
    /* Executed on EPFL drag events if extras_handle_drag is set to true. Overwrite to provide behaviour when dragging
       is started. */
};

epfl.ComponentBase.prototype.handle_keyup = function (event) {
    /* Executed on EPFL keyup event, overwrite to provide behaviour on keyup event */
};
