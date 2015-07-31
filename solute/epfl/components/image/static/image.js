epfl.Image = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
};
epfl.Image.inherits_from(epfl.ComponentBase);

Object.defineProperty(epfl.Image.prototype, 'img', {
    get: function () {
        return this.elm.find('img');
    }
});

epfl.Image.prototype.after_response = function() {
	if (this.params["show_dominant_color"] || this.params["show_additional_colors"]) {
		$('#'+cid).find('.epfl-img-component-image').imagesLoaded( function(instance) {
			var my_image = instance["images"][0].img;
			var colorThief = new ColorThief();
			if (params["show_dominant_color"]) {
				var dominantColor = colorThief.getColor(my_image);
				var dominant_color_div = $('#'+cid).find('.epfl-img-component-dominant-color');
				dominant_color_div.css("background-color", "rgb("+dominantColor+")");
			}
			if (params["show_additional_colors"]) {
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

$(".epfl-img-component-color").mouseover(function() {
	$(this).css({"border-width":"2px", "border-style":"solid"});
})
.mouseout(function() {
	$(this).css({"border-width":"0px", "border-style":"solid"});
});

