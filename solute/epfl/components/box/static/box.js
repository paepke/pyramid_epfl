epfl.Box = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Box.inherits_from(epfl.ComponentBase);


epfl.Box.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);

    if (!this.params.hover_box) {
        return;
    }
    if ($(event.target).parent().hasClass('epfl_box_remove_button') ||
       (this.params.hover_box_close_on_outside_click && !$(event.target).closest('#' + this.cid + ' .panel').length)) {
        // click on close button or outside of box
        if (this.params.hover_box_remove_on_close) {
            this.send_event("hide", {});
        } else {
            this.send_event("removed", {});
        }
        event.stopImmediatePropagation();
        event.preventDefault();
    }

};
