(function () {
    function get_epflid(containing_elm) {
        containing_elm = $(containing_elm);
        var cid = containing_elm.attr('epflid');
        if (!cid) {
            cid = containing_elm.parent().attr('epflid');
        }
        if (!cid) {
            cid = containing_elm.parentsUntil('[epflid]').parent().attr('epflid');
        }
        return cid;
    }

    function line_marker() {
        $('.drop-line-marker').remove();
        var arrow_l = $('<i class="pull-left fa fa-arrow-up" />');
        var arrow_r = $('<i class="pull-right fa fa-arrow-up" />');
        return $('<div></div>')
            .append(arrow_l)
            .append(arrow_r)
            .css('width', '100%')
            .css('height', '10px')
            .css('margin-top', '-10px')
            .css('overflow', 'show')
            .css('border-top', '1px solid black')
            .addClass('drop-line-marker')
            .mouseover(function (e) {
                e.stopPropagation();
            });
    }

    epfl.add_drop_zone = function (cid, position) {
        var done = false;
        var elm = $('[epflid=' + position[0] + ']');
        var parent = $('[epflid=' + cid + ']');

        if (!position[0]) {
            line_marker()
                .appendTo(parent);
        } else if (position[1]) {
            line_marker()
                .insertBefore(elm);
        } else {
            line_marker()
                .insertAfter(elm);
        }

        function mouseout(e) {
            if ($(e.target).attr('epflid') != parent.attr('epflid')) {
                return;
            }
            $(this).unbind('mouseout', mouseout);
            $('.drop-line-marker').remove();
        }

        parent.mouseout(mouseout);
    };

    var old_cid = '';

    epfl.set_drop_zone_parent = function (elm, dragged) {
        var drop_zone_parent = $(elm);
        var dragged_element = $(dragged);

        var cid = get_epflid(drop_zone_parent);
        if (cid == old_cid) {
            return;
        }
        old_cid = cid;
        epfl.send(epfl.make_component_event(cid, 'drop_accepts', {cid: dragged_element.attr('epflid')}));
    };
})();