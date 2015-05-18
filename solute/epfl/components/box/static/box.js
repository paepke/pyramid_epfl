epfl.Box = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Box.inherits_from(epfl.ComponentBase);

epfl.Box.prototype.is_hover_box = function () {
    return this.elm.hasClass('epfl_hover_box');
};


epfl.Box.prototype.handle_remove = function (event) {
    epfl.dispatch_event(this.cid, "removed", {});
};

epfl.Box.prototype.handle_hide = function (event) {
    epfl.dispatch_event(this.cid, "hide", {});
};

epfl.Box.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);

    if (!$(event.target).parent().hasClass('epfl_box_remove_button')) {
        return;
    }
    event.stopImmediatePropagation();
    event.preventDefault();

    if (this.is_hover_box() && !this.params.hover_box_remove_on_close) {
        epfl.dispatch_event(this.cid, "hide", {});
    } else {
        epfl.dispatch_event(this.cid, "removed", {});
    }
};
