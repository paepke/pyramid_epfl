epfl.make_compo_dragable = function (cid, params) {
	keep_in_place=params["keep_orig_in_place"];
    $('[epflid=' + cid +  ']').mousedown(function (e) {
        function reset_css() {
        	if (elm_copy) {
        		elm_copy.remove();
        	}
            elm.css('position', style_before['position']);
            elm.css('left', style_before['left']);
            elm.css('top', style_before['top']);
            elm.css('z-index', style_before['zIndex']);
        }

        function update_css(x, y) {
        	local_elm = elm;
        	if (elm_copy) {
        		local_elm=elm_copy;
        		elm.removeClass("placeholder");
        	}
            local_elm.css('position', 'fixed');
            local_elm.css('left', x + 'px');
            local_elm.css('top', y + 'px');
            local_elm.css('z-index', 100);
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
        var elm = $(this);
        var elm_copy;
			

        var style_before = {position: elm.css('position'),
                            left: elm.css('left'),
                            top: elm.css('top'),
                            zIndex: elm.css('z-index')};
        var x = e.clientX;
        var y = e.clientY;

        if (get_epflid(e.target) != elm.attr('epflid')) {
            return;
        }
        e.preventDefault();

        $(document)
            .mousemove(function (e) {
                e.preventDefault();
                if (e.clientX - x < 5 && e.clientX - x > -5
                    && e.clientY - y < 5 && e.clientY - y > -5) {
                    return reset_css();
                }
                if (keep_in_place && !elm_copy) {
					elm_copy = elm.clone().appendTo(elm.parent());
					elm.addClass('placeholder');
					elm_copy.addClass('dragged');
					elm_copy.css('width', elm.width() + 'px');
				}
                update_css(e.clientX + 5, e.clientY + 5);
            })
            .mouseup(function (e) {
                var containing_elm = $(e.target);
                $(document).unbind('mousemove');
                $(document).unbind('mouseover');
                $(document).unbind('mouseup');
                var cid = get_epflid(e.target);
                if (cid
                    && (e.clientX - x >= 5 || e.clientX - x <= -5
                    || e.clientY - y >= 5 || e.clientY - y <= -5) ) {
                    epfl.dispatch_event(cid, 'drag_stop', {cid: elm.attr('epflid'),
                                                           over_cid: get_epflid(containing_elm)});
                }
                reset_css();
            })
            .mouseover(function (e) {
                var cid = get_epflid(e.target);
                if (!cid) {
                    return;
                }
                e.stopImmediatePropagation();

                epfl.dispatch_event(cid, 'drop_accepts', {cid: elm.attr('epflid'),
                                                          elm: elm,
                                                          originalEvent: e});
            });
    });
};