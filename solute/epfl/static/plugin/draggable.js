/*
    Epfl Plugin Wrapper for jqueryui draggable
    the element with the selector gets draggable
    the selector element must have an epflid
    customClass is added to the original element while dragging and got removed after drag
 */

epfl.PluginDraggable = function (selector, customClass) {
    $(selector).draggable({
        revert: "invalid",
        scroll: false,
        helper: 'clone',
        cursorAt: {top: -5, left: -5},
        containment: "window",
        zIndex: 5000,
        scroll: true,
        start: function (event, ui) {
            if(customClass) {
                $(this).addClass(customClass);
            }
        },
        stop: function (event, ui) {
            if(customClass) {
                $(this).removeClass(customClass);
            }
        },
        appendTo: "body"
    });
};

