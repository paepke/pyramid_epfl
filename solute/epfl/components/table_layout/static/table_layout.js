epfl.TableLayout = function (cid, params) {
    epfl.PaginatedListLayout.call(this, cid, params);
    var compo = this;
    var selector = "#" + cid;
    if (params.fixed_header) {
        compo.enable_fixed_header_table = function () {
            var panel = $(selector);
            if (!panel.is(':visible')) {
                return setTimeout(compo.enable_fixed_header_table, 0);
            }

            $('#table_' + cid).fixedHeaderTable({autoShow: true, height: panel.height() - 80});
        };

        setTimeout(compo.enable_fixed_header_table, 0);
    }
};

epfl.TableLayout.inherits_from(epfl.PaginatedListLayout);

Object.defineProperty(epfl.TableLayout.prototype, 'hide_column_icon', {
    get: function () {
        return this.elm.find('.hide-column-icon');
    }
});

Object.defineProperty(epfl.TableLayout.prototype, 'show_column_icon', {
    get: function () {
        return this.elm.find('.show-column-icon');
    }
});

epfl.TableLayout.prototype.handle_click = function (event) {
    epfl.PaginatedListLayout.prototype.handle_click.call(this, event);
    if (this.hide_column_icon.is(event.target) ) {
        var parent_col = event.target.closest("th");
        this.send_event("hide_column", {column_index: $(parent_col).index()});
    } else if (this.show_column_icon.is(event.target)) {
        var parent_col = event.target.closest("th");
        this.send_event("show_column", {column_index: $(parent_col).index()});
    }

};
