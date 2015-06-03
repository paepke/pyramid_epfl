epfl.SelectableList = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var selector = "#" + cid;
    var compo = this;

    $(selector + " a").click(function () {
        var evt = epfl.make_component_event(cid, "select", {cid: $(this).attr("epflid")});
        epfl.send(evt);
    }).dblclick(function(){
        var evt = epfl.make_component_event(cid, "double_click", {cid: $(this).attr("epflid")});
        epfl.send(evt);
    });

};

epfl.SelectableList.inherits_from(epfl.ComponentBase);
