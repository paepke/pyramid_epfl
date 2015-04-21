epfl.TableLayout = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
	var compo = this;
    var selector = "#" + cid;
    var panel = $(selector + '_panel');
	var panel_height = panel.height();
    $(selector).fixedHeaderTable({autoShow: true, height: panel_height - 80, themeClass: 'deal-table'});
}; 
epfl.TableLayout.inherits_from(epfl.ComponentBase);

