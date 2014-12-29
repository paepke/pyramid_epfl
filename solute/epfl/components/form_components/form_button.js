$('[id="{{compo.cid}}"]').click(function(event) {
    var request = epfl.make_component_event("{{compo.callback[0]}}", "{{compo.callback[1]}}");
    epfl.send(request);
});
