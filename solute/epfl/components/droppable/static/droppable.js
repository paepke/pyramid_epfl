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
            if (epfl.components[$(this).attr('id')].block_cid(ui.item.attr('epflid'))) {
                return;
            }
            var parent_epflid = ui.item.parent().attr('id');
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
        $('[epflid="'+cid+'"] > .toggle-list').click(function(event) {
        	event.stopImmediatePropagation();
        	event.preventDefault();
        	$('#'+cid).toggle().sortable('disable').sortable('enable');
        	$(this).children('i').toggleClass('fa-minus').toggleClass('fa-plus');
        	
  			var ev = compo.make_event("toggle_collapse",{"collapsed":!$('#'+cid).is(":visible")});
        	epfl.send(ev);
        });
        $('[epflid="'+cid+'"] > .title-rename.inactive').bind('dblclick keyup', function(event) {
        	if ((event.type == "keyup") && (event.keyCode != 113)) { // F2
				return;
			}
        	$(this).removeClass("inactive");
        });
		$('[epflid="'+cid+'"] > .title-rename').bind('keyup', function(event){
			if ((event.keyCode != 13) && (event.keyCode != 27)) {
				return;
			}
			if (event.keyCode == 27) { // ESC, undo changes
				$(this).val($(this).data("oldtitle"));
			}
			$(this).blur(); // will trigger focusout event
		});
		$('[epflid="'+cid+'"] > .title-rename').bind('focusout', function(event){

			if ($(this).hasClass("inactive")) {
				return;
			}
			
			$(this).addClass("inactive");
			if ($(this).data("oldtitle") != $(this).val()) {
				$(this).data("oldtitle", $(this).val());
    			var ev = compo.make_event("rename_title",{"title":$(this).val()});
    			epfl.send(ev);
    		}
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