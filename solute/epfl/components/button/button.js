$('[id="{{compo.cid}}"]').click(function(event) {
    var request = epfl.make_component_event("{{compo.event_target}}", "{{compo.event_name}}");
    epfl.send(request);
});
