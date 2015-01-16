$('[epflid="{{compo.cid}}"]').submit(function(event) {
    event.preventDefault();
    var request = epfl.make_component_event("{{compo.cid}}", "submit", {});
    epfl.send(request);
});
