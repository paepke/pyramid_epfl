epfl.ColorThief = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.ColorThief.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.ColorThief.prototype, 'color_field', {
    get: function () {
        return this.elm.children('div.epfl-colorthief-color');
    }
});

Object.defineProperty(epfl.ColorThief.prototype, 'check_icon', {
    get: function () {
        return this.elm.children('div').children('i.fa-check');
    }
});

Object.defineProperty(epfl.ColorThief.prototype, 'remove_icon', {
    get: function () {
        console.log(this.elm.children('i.epfl-colorthief-remove-icon'));
        return this.elm.children('i.epfl-colorthief-remove-icon');
    }
});

epfl.ColorThief.prototype.handle_click = function (event) {
    epfl.ComponentBase.prototype.handle_click.call(this, event);
    var target = $(event.target);
    if (this.color_field.is(event.target)) {
        this.send_event("click_color", {"color": target.data("color")});
    } else if (this.check_icon.is(event.target)) {
        this.send_event("click_color", {"color": target.parent().data("color")});
    } else if (this.remove_icon.is(event.target)) {
        this.send_event("change", {value: null})
    }

};

epfl.ColorThief.prototype.handle_drop = function (event) {
    epfl.ComponentBase.prototype.handle_drop.call(this, event);
    var imageSrc = $(event.dataTransfer.getData('text/html')).attr("src");
    var image = this.elm.find("img");
    if (imageSrc) {
        image.attr("src", imageSrc);
        var colorThief = new ColorThief();
        var dominantColors = colorThief.getPalette(image[0], parseInt(this.params["color_count"]));
        this.send_event("change", {"value": dominantColors, "image_src": imageSrc})
    }
};
