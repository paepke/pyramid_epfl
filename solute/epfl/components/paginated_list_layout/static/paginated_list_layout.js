epfl.PaginatedListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var compo = this;
    var elm = $('[epflid=' + cid + ']');

    function send_row_update(data, callback) {
        var _data = {
            row_data: params.row_data,
            row_limit: params.row_limit,
            row_offset: params.row_offset
        };
        for (var key in data) {
            _data[key] = data[key];
        }
        epfl.send(compo.make_event('set_row', _data), callback);
    }

    function submit() {
        try {
            if (search_elm.val() == params.row_data['search']) {
                return;
            }
        } catch (e) {
        }

        if (search_elm.prev().prop("tagName") != "SPAN") {
            search_elm
                .before($("<span></span>")
                    .addClass("fa fa-spinner fa-spin")
                    .css("margin-right", "25px")
            );
        }
        var row_data = params.row_data;
        if (!row_data) {
            row_data = {};
        }

        if ($("#" + cid + "_orderby").length && $("#" + cid + "_ordertype").length) {
            row_data.orderby = $("#" + cid + "_orderby option:selected").val();
            row_data.ordertype = $("#" + cid + "_ordertype option:selected").val();
        }

        row_data.search = search_elm.val();
        send_row_update({row_data: row_data}, function () {
            if (search_elm && search_elm.prev().prop("tagName") == "SPAN") {
                search_elm.prev().remove();
                search_elm.parent().removeClass("has-feedback");
            }
        });
    }

    if (params.show_search) {
        var search_timeout;
        var search_elm = $('#' + cid + '_search');
        var preventSubmit = function(event) {
            if (event.key == 'Enter') {
                event.preventDefault();
                return false;
            }
        };
        search_elm.keyup(function (event) {
            if (search_timeout) {
                clearTimeout(search_timeout);
            }
            if (event.key == 'Enter') {
                submit();
                return preventSubmit(event);
            } else {
                search_timeout = setTimeout(submit, 500);
            }
        });
        search_elm.keypress(preventSubmit);
        search_elm.keydown(preventSubmit);

        if (params.search_focus) {
            // Bugfix: focus fails if triggered without this timeout.
            setTimeout(function () {
                search_elm.focus();
                search_elm[0].setSelectionRange(search_elm.val().length, search_elm.val().length);
            });
        }
    }
    if (params.show_pagination) {
        var pagination_elm = $('#' + cid + '_pagination');
        pagination_elm.click(function (event) {
            if ($(event.target.parentNode).hasClass('disabled')) {
                return;
            }
            var target_string = event.target.textContent;
            var selected_offset;
            switch (target_string) {
                case '«':
                    selected_offset = 0;
                    break;
                case '»':
                    selected_offset = Math.floor(params.row_count / params.row_limit);
                    break;
                case '<':
                    selected_offset = Math.floor(params.row_offset / params.row_limit) - 1;
                    break;
                case '>':
                    selected_offset = Math.floor(params.row_offset / params.row_limit) + 1;
                    break;
                default:
                    selected_offset = parseInt(target_string) - 1;
            }
            if (selected_offset * params.row_limit != params.row_offset) {
                send_row_update({row_offset: selected_offset * params.row_limit})
            }
        });
    }
};
epfl.PaginatedListLayout.inherits_from(epfl.ComponentBase);
