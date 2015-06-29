epfl.SelectableList = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid;
    var scrollArea = selector + " > .epfl-list";
    var compo = this;
    var scrollTimeout = null;

    $(selector + " a").click(function () {
        var evt = epfl.make_component_event(cid, "select", {cid: $(this).attr("epflid")});
        epfl.send(evt);
    }).dblclick(function(){
        var evt = epfl.make_component_event(cid, "double_click", {cid: $(this).attr("epflid")});
        epfl.send(evt);
    });

    $(scrollArea).scroll(function () {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function(){
            epfl.enqueue(compo.make_event('scroll', {scroll_pos: $(scrollArea).scrollTop()}));
        },250);
    });

    if(params["scroll_pos"]) {
        $(scrollArea).scrollTop(params["scroll_pos"]);
    }
};

epfl.SelectableList.inherits_from(epfl.ComponentBase);
