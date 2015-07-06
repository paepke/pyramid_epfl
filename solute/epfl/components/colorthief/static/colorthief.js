epfl.ColorThief = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.ColorThief.inherits_from(epfl.ComponentBase);


epfl.ColorThief.prototype.handle_drop_file = function (files, event) {
};


epfl.ColorThief.prototype.handle_drop_url = function (url, event) {
};

epfl.ColorThief.prototype.handle_click = function (event) {
    epfl.ComponentBase.prototype.handle_click.call(this, event);
    if ($(event.target).hasClass("epfl-colorthief-color")) {
        epfl.send(epfl.make_component_event(this.cid, "click_color", {"color": $(event.target).data("color")}));
    }
};

epfl.ColorThief.prototype.handle_drop = function (event) {
    epfl.ComponentBase.prototype.handle_drop.call(this, event);
    var imageSrc = $(event.dataTransfer.getData('text/html')).attr("src");
    var image = this.elm.find("img");
    if (imageSrc) {
        image.attr("src", imageSrc);
        var colorThief = new ColorThief();
        var dominantColors = colorThief.getPalette(image[0], parseInt(this.params["colors_count"]));
        epfl.send(epfl.make_component_event(this.cid, "change", {"value": dominantColors, "image_src": imageSrc}));
    }

};
