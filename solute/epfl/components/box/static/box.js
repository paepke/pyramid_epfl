epfl.Box = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Box.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Box.prototype, 'close_icon', {
    get: function () {
        return this.elm.find('> .panel > .panel-heading > .epfl_box_remove_button > i').add(
            this.elm.find('> .panel > .epfl_box_remove_button > i'));
    }
});

epfl.Box.prototype.handle_local_click = function (event) {
    epfl.ComponentBase.prototype.handle_local_click.call(this, event);

    if (!this.params.hover_box) {
        return;
    }
    if ((this.elm.is(event.target)) || (this.close_icon.is(event.target))) {
        // click on close button or outside of box
        if (this.params.hover_box_remove_on_close) {
            this.send_event("removed", {});
        } else {
            this.send_event("hide", {});
        }
        event.stopImmediatePropagation();
        event.preventDefault();
    }

};
