epfl.DroppableComponent = function (cid, params) {
    var blocked_compos = {};
    var compo = this;
    this.blocked = 0;
    epfl.ComponentBase.call(this, cid, params);
    $('#' + cid)
        .sortable({
            connectWith: params.type,
            placeholder: "ui-state-highlight",
            forcePlaceholderSize: true
        })
        .on('sortstop', function (event, ui) {
            if (epfl.components[$(this).attr('epflid')].block_cid(ui.item.attr('epflid'))) {
                return;
            }
            var parent_epflid = ui.item.parent().attr('epflid');
            //console.log("Sort new - EPFLID: " + ui.item.attr('epflid') + " | Position: " + ui.item.index());
            var evt = epfl.components[parent_epflid].make_event('add_dragable', {
                cid: ui.item.attr('epflid'),
                position: ui.item.index()});
            epfl.send(evt);
        })
        .on('sortactivate', function (event, ui) {
            $(this).addClass('list-group-active');
            $(this).css('min-height', ui.item.height() + 'px');
//            $(this).css('padding-bottom', Math.max(ui.item.height(), 20) + 'px');
        })
        .on('sortdeactivate', function (event, ui) {
            $(this).removeClass('list-group-active');
            $(this).css('min-height', '');
//            $(this).css('padding-bottom', '');
        });
        // handle collapsable droppables
        $('[epflid="'+cid+'"]').find('.toggle-list').first().click(function(event) {
        	$('[epflid="'+cid+'"]').find('.list-contents').first().toggle();
        	is_collapsed = !($('[epflid="'+cid+'"]').find('.list-contents').first().is(":visible"));
        	if (is_collapsed) {
        		$('[epflid="'+cid+'"]').find('.toggle-list i').first().html("&#xf196;");
        	} else {
        		$('[epflid="'+cid+'"]').find('.toggle-list i').first().html("&#xf147;");
        	}
        	
  			var ev = compo.make_event("toggle_collapse",{"collapsed":is_collapsed});
        	epfl.send(ev);
        });
};
epfl.DroppableComponent.inherits_from(epfl.ComponentBase);

var droppable_blocked_cid = {};

epfl.DroppableComponent.prototype.block_cid = function (cid) {
    var result = droppable_blocked_cid[cid] > 0;
    if (!droppable_blocked_cid[cid]) {
        droppable_blocked_cid[cid] = 0;
    }
    droppable_blocked_cid[cid]++;

    window.setTimeout("droppable_blocked_cid['" + cid + "']--;", 10);

    return result;
};