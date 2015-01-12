epfl.TableLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;

    epfl.TableLayout.buttonClickHandler = function (eventname) {
        var evt = compo.make_event(eventname, {});
        epfl.send(evt);
    }
};

epfl.TableLayout.inherits_from(epfl.ComponentBase);

epfl.TableLayout.prototype.fire_event = function (event_name, params, callback_fn) {
    if (!params) {
        params = {}
    }

    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.init_component("{{compo.cid}}", "TableLayout", {});


