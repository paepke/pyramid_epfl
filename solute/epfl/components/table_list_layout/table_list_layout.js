epfl.TableListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;

    epfl.TableListLayout.buttonClickHandler = function (eventname) {
        var evt = compo.make_event(eventname, {});
        epfl.send(evt);
    };
    epfl.TableListLayout.EditClick = function (id,data) {
        var evt = compo.make_event("edit", {'id':id,'data':data});
        epfl.send(evt);
    };
    var orderchange = function(){
        var orderby = $("#{{ compo.cid }}_orderby option:selected").val();
        var ordertype = $("#{{ compo.cid }}_ordertype option:selected").val();
        var search = $("#{{ compo.cid }}_search").val();
        var evt = compo.make_event("set_row", {
            row_offset: {{ compo.row_offset }},
            row_limit: {{ compo.row_limit }},
            row_data: {"search":search,"orderby": orderby,"ordertype": ordertype}
        });
        epfl.send(evt);
    };

    $("#{{ compo.cid }}_orderby").change(orderchange);
    $("#{{ compo.cid }}_ordertype").change(orderchange);


};

epfl.TableListLayout.inherits_from(epfl.ComponentBase);

epfl.TableListLayout.prototype.fire_event = function (event_name, params, callback_fn) {
    if (!params) {
        params = {}
    }

    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.init_component("{{compo.cid}}", "TableListLayout", {});
