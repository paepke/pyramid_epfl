epfl.TableListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;

    var orderchange = function () {
        var orderby = $("#{{ compo.cid }}_orderby option:selected").val();
        var ordertype = $("#{{ compo.cid }}_ordertype option:selected").val();
        var search = $("#{{ compo.cid }}_search").val();
        var evt = epfl.make_component_event("{{ compo.cid }}", "set_row", {
            row_offset: {{ compo.row_offset }},
            row_limit: {{ compo.row_limit }},
            row_data: {"search": search, "orderby": orderby, "ordertype": ordertype}
        });
        epfl.send(evt);
    };

    $("#{{ compo.cid }}_orderby").change(orderchange);
    $("#{{ compo.cid }}_ordertype").change(orderchange);


};

epfl.TableListLayout.OrderByClick = function (orderby) {
    if (epfl.TableListLayout.CurrentOrderBy == orderby) {
        if (epfl.TableListLayout.CurrentOrderByDirection == 'asc') {
            epfl.TableListLayout.CurrentOrderByDirection = 'desc';
        } else {
            epfl.TableListLayout.CurrentOrderByDirection = 'asc';
        }
    } else {
        epfl.TableListLayout.CurrentOrderByDirection = 'asc';
        epfl.TableListLayout.CurrentOrderBy = orderby;
    }
    var orderby = orderby;
    var ordertype = epfl.TableListLayout.CurrentOrderByDirection;
    var search = $("#{{ compo.cid }}_search").val();

    $("#{{ compo.cid }}_orderby [value='"+orderby+"']").attr('selected', 'selected');
    $("#{{ compo.cid }}_ordertype [value='"+ordertype+"']").attr('selected', 'selected');

    var evt = epfl.make_component_event("{{ compo.cid }}", "set_row", {
        row_offset: {{ compo.row_offset }},
        row_limit: {{ compo.row_limit }},
        row_data: {"search": search, "orderby": orderby, "ordertype": ordertype}
    });
    epfl.send(evt);
};


epfl.TableListLayout.buttonClickHandler = function (eventname) {
    var evt = epfl.make_component_event("{{ compo.cid }}", eventname, {});
    epfl.send(evt);
};
epfl.TableListLayout.EditClick = function (id, data) {
    var evt = epfl.make_component_event("{{ compo.cid }}", "edit", {'id': id, 'data': data});
    epfl.send(evt);
};


epfl.TableListLayout.exportCSV = function () {
    var evt = epfl.make_component_event("{{ compo.cid }}", "export_csv", {});
    epfl.send(evt);
};

epfl.TableListLayout.CurrentOrderBy = null;
epfl.TableListLayout.CurrentOrderByDirection = "asc";

epfl.TableListLayout.inherits_from(epfl.ComponentBase);

epfl.TableListLayout.prototype.fire_event = function (event_name, params, callback_fn) {
    if (!params) {
        params = {}
    }

    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.init_component("{{compo.cid}}", "TableListLayout", {});
