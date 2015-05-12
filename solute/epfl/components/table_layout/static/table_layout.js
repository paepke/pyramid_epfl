epfl.TableLayout = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
	var compo = this;
    var selector = "#" + cid;

    compo.enable_fixed_header_table = function () {
        var panel = $(selector);
        if (!panel.is(':visible')) {
            return setTimeout(compo.enable_fixed_header_table, 0);
        }

        $('#table_' + cid).fixedHeaderTable({autoShow: true, height: panel.height() - 80});
    };

    setTimeout(compo.enable_fixed_header_table, 0);
}; 
epfl.TableLayout.inherits_from(epfl.ComponentBase);

