/**
 * Created by mast on 06.02.15.
 */
epfl.TableListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var orderchange = function () {
        var orderby = $("#" + cid + "_orderby option:selected").val();
        var ordertype = $("#" + cid + "_ordertype option:selected").val();
        var search = $("#" + cid + "_search").val();
        epfl.dispatch_event(cid, "set_row", {
            row_offset: params['row_offset'],
            row_limit: params['row_limit'],
            row_data: {"search": search, "orderby": orderby, "ordertype": ordertype}
        });
    };

    $("#" + cid + "_orderby").change(orderchange);
    $("#" + cid + "_ordertype").change(orderchange);

    $(function () {
        $('[data-toggle="popover"]').popover()
    });

    $(".tablelistlayout-sortcolumn").click(function (evt) {
        var orderby = $(this).text().trim();

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
        var search = $("#" + cid + "_search").val();

        $("#" + cid + "_orderby [value='" + orderby + "']").attr('selected', 'selected');
        $("#" + cid + "__ordertype [value='" + ordertype + "']").attr('selected', 'selected');

        epfl.dispatch_event(cid, "set_row", {
            row_offset: params['row_offset'],
            row_limit: params['row_limit'],
            row_data: {"search": search, "orderby": orderby, "ordertype": ordertype}
        });
    });

    epfl.TableListLayout.buttonClickHandler = function (eventname) {
        epfl.dispatch_event(cid, eventname, {});
    };
    epfl.TableListLayout.EditClick = function (id, data) {
        epfl.dispatch_event(cid, 'edit', {'entry_id': id, 'data': data});
    };


    epfl.TableListLayout.exportCSV = function () {
        epfl.dispatch_event(cid, "export_csv", {});
    };
};


epfl.TableListLayout.inherits_from(epfl.ComponentBase);

epfl.TableListLayout.CurrentOrderBy = null;
epfl.TableListLayout.CurrentOrderByDirection = "asc";