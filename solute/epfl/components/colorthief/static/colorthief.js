epfl.ColorThief = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);


    //jquery selectors
    var selector = "#" + cid;
    var dropZone = $(selector + " div.epfl-colorthief-dropzone");
    var addIcon = $(selector + " p.epfl-dropzone-colorthief-addicon");
    var image = $(selector + " img");

    var that = this;


    var dragOverEvent = function (ev) {
        ev.preventDefault();
        addIcon.hide();
        dropZone.css({"border-color": "#1BB7A0"});
    };

    //drag file out event
    var dragLeaveEvent = function (ev) {
        ev.preventDefault();
        addIcon.show();
        dropZone.css({"border-color": "#D7D7D7"});
    };

    var dropEvent = function (ev) {
        ev.preventDefault();

        //show the image and hide the plus icon
        addIcon.hide();
        dropZone.hide();

        //get the html tag of the dragged image
        var dataTransfer = $(ev.dataTransfer.getData('text/html'));

        //extract src and check if the image is from a epfl compo
        var url = dataTransfer.attr("src");
        image.attr("src",url);
        console.log("image",image,parseInt(params["colors_count"]),params);
        var colorThief = new ColorThief();
        var dominantColors = colorThief.getPalette(image[0], parseInt(params["colors_count"]));


        epfl.send(
                epfl.make_component_event(
                        that.cid,
                        "change", {
                            "value": dominantColors,
                            "image_src": url
                        }
                )
        );

    };


    //Drop Zone Events
    dropZone.on("dragover", dragOverEvent);
    dropZone.on("dragleave", dragLeaveEvent);
    dropZone.on('drop', dropEvent);

};
epfl.ColorThief.inherits_from(epfl.FormInputBase);

epfl.ColorThief.prototype.handle_local_click = function (event) {
    console.log("CLICK COLORTHIEF");
    epfl.FormInputBase.prototype.handle_local_click.call(this, event);

};