epfl.Popover = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $('#'+cid+"_popover").popover();
};

epfl.Popover.inherits_from(epfl.ComponentBase);


