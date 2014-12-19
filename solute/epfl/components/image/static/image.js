epfl.ImageComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    
	if ((params["opts"]["show_dominant_color"]) || (params["opts"]["show_additional_colors"])) {
		$('[epflid="'+cid+'"]').find('.epfl-img-component-image').imagesLoaded( function(instance) {
			var my_image = instance["images"][0].img;
			var colorThief = new ColorThief();
			if (params["opts"]["show_dominant_color"]) {
				var dominantColor = colorThief.getColor(my_image);
				var dominant_color_div = $('[epflid="'+cid+'"]').find('.epfl-img-component-dominant-color');
				dominant_color_div.css("background-color", "rgb("+dominantColor+")");
			}
			if (params["opts"]["show_additional_colors"]) {
				var additionalColors = colorThief.getPalette(my_image, 8);
				// skip the first color, it is the dominant color
				for (var i = 1; i < additionalColors.length; i++) {
				    var palette_div = $('#' + cid + '_palette'+i);
					palette_div.css("background-color", "rgb("+additionalColors[i]+")");
				}
			}
		});
	}
};
epfl.ImageComponent.inherits_from(epfl.ComponentBase);

epfl.ImageComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

$(".epfl-img-component-color").mouseover(function() {
	$(this).css({"border-width":"2px", "border-style":"solid"});
})
.mouseout(function() {
	$(this).css({"border-width":"0px", "border-style":"solid"});
});

