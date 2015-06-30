epfl.ColorThief = function (cid, params) {
    epfl.FormInputBase.call(this, cid, params);
     console.log("RELOAD COLORTHIEF");
};
epfl.ColorThief.inherits_from(epfl.FormInputBase);

epfl.ColorThief.prototype.handle_local_click = function (event) {
    console.log("CLICK COLORTHIEF");
    epfl.FormInputBase.prototype.handle_local_click.call(this, event);

};