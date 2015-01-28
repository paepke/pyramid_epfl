epfl.TableListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var orderchange = function () {
        var orderby = $("#" + cid + "_orderby option:selected").val();
        var ordertype = $("#" + cid + "_ordertype option:selected").val();
        var search = $("#" + cid + "_search").val(); 
        epfl.dispatch_event(cid, "set_row", {
            row_offset: {{ compo.row_offset }},
            row_limit: {{ compo.row_limit }},
            row_data: {"search": search, "orderby": orderby, "ordertype": ordertype}
        });
         
    };

    $("#" + cid + "_orderby").change(orderchange);
    $("#" + cid + "_ordertype").change(orderchange);


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

    epfl.dispatch_event("{{ compo.cid }}", "set_row", {
        row_offset: {{ compo.row_offset }},
        row_limit: {{ compo.row_limit }},
        row_data: {"search": search, "orderby": orderby, "ordertype": ordertype}
    });
};


epfl.TableListLayout.buttonClickHandler = function (eventname) {
    epfl.dispatch_event("{{ compo.cid }}", eventname, {});
};
epfl.TableListLayout.EditClick = function (id, data) {
	epfl.dispatch_event("{{ compo.cid }}", 'edit', {'id': id, 'data': data});
};


epfl.TableListLayout.exportCSV = function () {
    epfl.dispatch_event("{{ compo.cid }}", "export_csv", {});
};

epfl.TableListLayout.CurrentOrderBy = null;
epfl.TableListLayout.CurrentOrderByDirection = "asc";

epfl.TableListLayout.inherits_from(epfl.ComponentBase);

epfl.init_component("{{compo.cid}}", "TableListLayout", {});
