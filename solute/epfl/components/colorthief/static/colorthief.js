epfl.ColorThief = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.ColorThief.inherits_from(epfl.ComponentBase);

epfl.ColorThief.prototype.handle_click = function (event) {
    epfl.ComponentBase.prototype.handle_click.call(this, event);
    var target = $(event.target);
    if (target.hasClass("epfl-colorthief-color")) {
        epfl.send(epfl.make_component_event(this.cid, "click_color", {"color": target.data("color")}));
    }else if(target.hasClass("fa-check")){
        epfl.send(epfl.make_component_event(this.cid, "click_color", {"color": target.parent().data("color")}));
    }else if(target.hasClass("epfl-colorthief-remove-icon")){
        epfl.send(epfl.make_component_event(this.cid, "change", {"value": null, "image_src": null}));
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
        epfl.send(epfl.make_component_event(this.cid, "change", {"value": dominantColors, "image_src": imageSrc}));
    }
};
