
epfl.SortWidget = function(wid, cid, params) {
    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    this.update_hidden_fields();

    var el = $( "#" + params.name );
    el.sortable();
    el.disableSelection();
    if (params.on_click) {
        el.on("click", function(event, ui) {
            if (event.target.getAttribute("idx")) {
                var el = event.target;
            } else {                
                var el = event.target.parentNode;
            }
            var idx = $( "#" + widget_obj.name ).children().index(el); // here the "real" index is needed, not the
                                                                       // "idx"-attribute used for sorting
            var ev = widget_obj.make_event.call(widget_obj, "onClick", {"idx": idx});
            epfl.send(ev);
        });
    };
    el.on( "sortstop", function( event, ui ) {
        widget_obj.update_hidden_fields.call(widget_obj);
        widget_obj.notify_value_change.call(widget_obj);
        if (params.on_change) {
            var ev = widget_obj.make_event.call(widget_obj, "onChange");
            epfl.send(ev);
        };
    } );


}
epfl.SortWidget.inherits_from(epfl.WidgetBase);


epfl.SortWidget.prototype.update_hidden_fields = function() {
    var widget_obj = this;

    var el = $( "#" + this.name );
    $("._hv_" + this.name).remove();

    el.children().each(function() {
        var idx = this.getAttribute("idx");
        $('<input>').attr({'type': 'hidden',
                           'name': "_idx_" + widget_obj.name,
                           'class': '_hv_' + widget_obj.name,
                           'value': idx}).appendTo(el);
    });
};


epfl.SortWidget.prototype.get_value = function() {
    var value = [];

    $( "#" + this.name ).children().each(function() {
        var idx = parseInt(this.getAttribute("idx"));
        if (!isNaN(idx)) {
            value.push(idx);
        };
    });
    return value;
};

epfl.SortWidget.prototype.reset_idx = function() {
    var new_idx = 0;
    $( "#" + this.name ).children().each(function() {
        var idx = parseInt(this.getAttribute("idx"));
        if (!isNaN(idx)) {
            this.setAttribute("idx", new_idx);
            new_idx += 1;
        };
    });
};
