$('[epflid="{{compo.cid}}"]').submit(function(event) {
    event.preventDefault();
    epfl.dispatch_event("{{compo.cid}}", "submit", {});
});
