epfl.selectable_list_click = function(elm,cid) {
    var evt = epfl.make_component_event(elm, "select", {cid:cid});
    epfl.send(evt);
};
