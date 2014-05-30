
epfl.BasicWidget = function(wid, cid, params) {

	var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

	this.typ = params.typ;

	if (this.typ == "button") {

		// Javascript for buttons
        if (this.get_param("on_click") == "submit") {
            $("#" + this.wid).click(function() {
            	var compo = widget_obj.get_form();
                compo.submit_form.call(compo, this.id);
            });
        } else if (this.get_param("on_click")) {
            $("#" + this.wid).click(function() {
                var ev = widget_obj.make_event("onClick", {});
                epfl.send(ev);
            });
        }

    } else if (this.typ == "radio") {

        // Javascript for radio buttons

        $("#" + this.wid).change(function() {

            widget_obj.notify_value_change.call(widget_obj);
            if (widget_obj.get_param("on_change")) {
                var ev = widget_obj.make_event("onChange");
                epfl.send(ev);
            };
        });

    } else if (this.typ == "entry") {

        var char_count_func = function() {
            var value = widget_obj.get_value();
            $("#" + widget_obj.wid + "_ccnt").html("(" + value.length + "/" + $("#" + widget_obj.wid).attr("maxlength") + ")");
        };

        // Javascript for entry-fields
        $("#" + this.wid).bind({

            keyup: function(e) {  // keyup event with timeout to prevent requests
                if (widget_obj.get_param("on_keyup")) {
                    var timer = $("#" + widget_obj.wid).data('timeout');

                    if(timer) {
                        clearTimeout(timer);
                        $("#" + widget_obj.wid).removeData('timeout');
                    }

                    if (e.which == 8 || $(this).val().length > 2) {
                        $("#" + widget_obj.wid).data('timeout', setTimeout(function(){
                            widget_obj.notify_value_change.call(widget_obj);
                            var ev = widget_obj.make_event("onKeyup");
                            epfl.send(ev);
                        }, 800));
                    }
                }
                // update char-count
                if (widget_obj.get_param("char_count")) { char_count_func(); };
            }});

        if (widget_obj.get_param("char_count")) {
            $("#" + this.wid).bind({
                cut: char_count_func,
                paste: char_count_func,
                change: char_count_func
            });
        };

        $("#" + this.wid).change(function() {  // onchange event
            widget_obj.notify_value_change.call(widget_obj);
            if (widget_obj.get_param("on_change")) {
                var ev = widget_obj.make_event("onChange");
                epfl.send(ev);
            };
        });

        $("#" + this.wid).keydown(function(e) {  // onchange event
            if (widget_obj.get_param("on_return")) {
                if (e.which == 13) {
                    widget_obj.notify_value_change.call(widget_obj);
                    var ev = widget_obj.make_event("onReturn");
                    epfl.send(ev);
                }
            };
        });

        char_count_func();

    } else if (this.typ == "textarea") {

        // Javascript for textarea-fields
        $("#" + this.wid).change(function() {
            widget_obj.notify_value_change.call(widget_obj);
        });

    } else if (this.typ == "buttonset") {
        $("#" + this.wid).buttonset();

        // Javascript for radiobutton groups
        $("#" + this.wid).change(function() {
            widget_obj.notify_value_change.call(widget_obj);
            if (widget_obj.get_param("on_change")) {
                var ev = widget_obj.make_event("onChange");
                epfl.send(ev);
            };
        });

    } else if (this.typ == "checkbox") {

        // Javascript for checkbox-fields
        $("#" + this.wid).on("change", function() {
            widget_obj.notify_value_change.call(widget_obj);
            if (widget_obj.get_param("on_change")) {
                var ev = widget_obj.make_event("onChange");
                epfl.send(ev);
            };
        });

    } else if (this.typ == "select") {

        // Javascript for select-fields
        $("#" + this.wid).change(function() {
            widget_obj.notify_value_change.call(widget_obj);
            if (widget_obj.get_param("on_change")) {
                var ev = widget_obj.make_event("onChange");
                epfl.send(ev);
            };
        });

    }

};
epfl.BasicWidget.inherits_from(epfl.WidgetBase);



epfl.BasicWidget.prototype.get_value = function() {
    if(this.typ == "checkbox") {
            return $( "#" + this.wid).prop('checked');
        } else if(this.typ == "buttonset", this.typ == "radio") {
            return $( "#" + this.wid + " input:checked").attr("id");
        }
    else {
        return $( "#" + this.wid).val();
    }
};