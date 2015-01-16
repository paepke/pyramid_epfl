$('[epflid=' + '{{ compo.cid }}]').mousedown(function (e) {
    e.preventDefault();
    var elm = $(this);

    var style_before = {position: elm.css('position'),
                        left: elm.css('left'),
                        top: elm.css('top')}
    var x = e.clientX;
    var y = e.clientY;

    function reset_css() {
        elm.css('position', style_before['position']);
        elm.css('left', style_before['left']);
        elm.css('top', style_before['top']);
    }

    function update_css(x, y) {
        elm.css('position', 'fixed');
        elm.css('left', x + 'px');
        elm.css('top', y + 'px');
    }

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

    if (get_epflid(e.target) != elm.attr('epflid')) {
        return;
    }

    $(document).mousemove(function (e) {
        e.preventDefault();
        if (e.clientX - x < 5 && e.clientX - x > -5
            && e.clientY - y < 5 && e.clientY - y > -5) {
            return reset_css();
        }
        update_css(e.clientX + 5, e.clientY + 5);
    });
    $(document).mouseup(function (e) {
        var containing_elm = $(e.target);
        $(document).unbind('mousemove');
        $(document).unbind('mouseup');
        var cid = get_epflid(e.target);
        if (cid
            && (e.clientX - x >= 5 || e.clientX - x <= -5
            || e.clientY - y >= 5 || e.clientY - y <= -5) ) {
            epfl.send(epfl.make_component_event(cid, 'drag_stop', {cid: elm.attr('epflid')}));
        }
        reset_css();
    });
});