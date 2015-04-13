epfl.PopoverContainer = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $('#' + cid + "_popover_container").popover({
        html:true
    });
    $('#' + cid + "_popover_container").on("remove", function () {
        $('#' + cid + "_popover_container").popover('destroy');
    })
};

epfl.PopoverContainer.inherits_from(epfl.ComponentBase);


