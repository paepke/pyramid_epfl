epfl.MultiSelect = function (cid, params) {
    if (params.scroll_position > 0) {
        $('#' + cid + ' > .list-group').scrollTop(params.scroll_position);
    }

    epfl.ComponentBase.call(this, cid, params);

    $('#' + cid + ' li.multiselect-selectable').click(function (event) {
        event.stopImmediatePropagation();
        event.preventDefault();

        var isSelected = $(this).hasClass("selected");
        $(this).toggleClass("selected");

        if (isSelected) {
            var child_cid = $(this).children().first().attr("epflid");
            epfl.enqueue(epfl.make_component_event(cid, 'unselected', {child_cid: child_cid}), cid);
        } else {
            var child_cid = $(this).children().first().attr("epflid");
            epfl.enqueue(epfl.make_component_event(cid, 'selected', {child_cid: child_cid}), cid);
        }
    }).dblclick(function(event){
        event.stopImmediatePropagation();
        event.preventDefault();
        var child_cid = $(this).children().first().attr("epflid");
        epfl.dispatch_event(cid, "double_click", {child_cid: child_cid});
    });

    // Remember scroll position
    $('#' + cid + ' ul.list-group').scroll(function () {
        clearTimeout($.data(this, 'multiselect_scrolltimer'));
        $.data(this, 'multiselect_scrolltimer', setTimeout(function () { // detect scroll stop
            epfl.enqueue(epfl.make_component_event(cid, "scrolled", {scroll_position: $('#' + cid + ' ul.list-group').scrollTop()}));
        }, 250));
    });
    // Search
    $('#' + cid + ' > .multiselect-search-input').keydown(function (event) {
        if (event.keyCode == 13) {
            epfl.dispatch_event(cid, "search", {search_string: $(this).val()});
        }
    });
};
epfl.MultiSelect.inherits_from(epfl.ComponentBase);
