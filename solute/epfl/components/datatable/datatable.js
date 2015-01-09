epfl.DataTableComponent = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;

   epfl.DataTableComponent.buttonClickHandler = function(eventname){
       var evt = compo.make_event(eventname,{});
       epfl.send(evt);
   }
};

epfl.DataTableComponent.inherits_from(epfl.ComponentBase);

epfl.DataTableComponent.prototype.fire_event = function (event_name, params, callback_fn) {
    if (!params) {
        params = {}
    }

    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.DataTableComponent.goto = function (element, cid, row_offset, row_limit, row_data) {
    var event = epfl.make_component_event(
        cid,
        'set_row',
        {
            row_offset: row_offset,
            row_limit: row_limit,
            row_data: row_data
        });
    epfl.send(event);
};

epfl.init_component("{{compo.cid}}", "DataTableComponent", {});


