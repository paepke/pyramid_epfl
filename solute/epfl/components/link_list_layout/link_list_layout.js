epfl.link_list_click = function(elm, event_name, event_target) {
    var evt = epfl.make_component_event(event_target, event_name, {});
    epfl.send(evt);
};
