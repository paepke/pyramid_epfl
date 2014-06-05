
epfl.SuggestWidget = function(wid, cid, params) {

    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    $("#" + wid + "__entry").autocomplete({
        source: function(request, response) {

            $("#" + wid).val("");

            var event = widget_obj.make_event("GetData", {"query": request.term});
            epfl.send(event, function(data) {

                var ac_data = [];

                for (var i = 0; i < data.length; i++){
                    ac_data.push({label: data[i][1],
                                  value: data[i][0]})
                }

                response(ac_data);
            });

        },


        select: function(event, ui) {
            var sel_obj = ui.item;
            $('#' + wid + "__entry").val(sel_obj.label);
            $('#' + wid).val(sel_obj.value);
            widget_obj.notify_value_change();
            return false;
        }
    });

    $("#" + wid + "__entry").change(function() {

        widget_obj.notify_value_change();
    });

    if (this.get_param("on_select")) {
        $("#" + wid + "__entry").on("suggestselect", function(e) {
            widget_obj.notify_value_change();
            var ev = widget_obj.make_widget_event("Select", {});
            epfl.send(ev);
        });
    }

    if (this.get_param("on_return")) {
        $("#" + wid + "__entry").keyup(function(e) {
            if(e.keyCode == 13) {
                var ev = widget_obj.make_event("onReturn", {});
                epfl.send(ev);
            }
        });
    }
};

epfl.SuggestWidget.inherits_from(epfl.WidgetBase);



epfl.SuggestWidget.prototype.get_value = function() {
    return {"value": $( "#" + this.wid).val(),
            "entry": $( "#" + this.wid + "__entry").val()}
};

