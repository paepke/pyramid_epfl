(function () {
    function get_epflid(containing_elm) {
        return $(containing_elm).closest('[epflid]').attr('epflid');
    }


    var drag_stop = function(cid) {
        return function (elm, type, data) {
            data.over_cid = $('[epflid=' + data.over_cid + ']')
                .closest('[epflid][data-parent-epflid=' + cid + ']').attr('epflid');
            return true;
        };
    };
    
    var marked_element;

    var remove_line_marker = function() {
        marked_element.removeClass('tree-drop-line-marker');
    };

    var drop_accepts = function(cid) {
        return function (elm, type, data) {
            var target_elm = $(data.originalEvent.target).closest('[epflid][data-parent-epflid=' + cid + ']');
            var target_cid = target_elm.attr('epflid');

            delete data.originalEvent;
            delete data.elm;
            if (typeof marked_element != "undefined") {
            	marked_element.removeClass('tree-drop-line-marker');
            }
            if (target_cid) {
            	marked_element = $('[epflid=' + target_cid + ']');
                
            } else {
                marked_element = $('[epflid=' + cid + ']');
            }
            marked_element.addClass('tree-drop-line-marker');

            elm.mouseout(function (e) {
                var elem = $(e.target);
                $(this).unbind('mouseout');
                remove_line_marker();
            });
        };
    };

    epfl.set_drop_zone = function (cid) {
        var elm = $('[epflid=' + cid + ']');

        epfl.set_component_info(cid, 'before_send_event', 'drop_accepts', drop_accepts(cid));
        epfl.set_component_info(cid, 'before_send_event', 'drag_stop', drag_stop(cid));
        epfl.set_component_info(cid, 'callback_send_event', 'drag_stop', remove_line_marker);
    };
})();