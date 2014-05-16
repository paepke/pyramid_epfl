epfl.AccordionWidget = function(wid, cid, params) {
    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    var field = $("#" + this.wid);

    // click on a section, this actually changes the field value
    if (this.get_param("on_section_click")) {
        var click_handler = function(event, ui) {
            widget_obj.notify_value_change.call(widget_obj);
            var ev = widget_obj.make_widget_event("SectionClick", {});
            epfl.send(ev);
        };
    } else {
        var click_handler = null;
    }

    // click on a content child
    if (this.get_param("on_content_click")) {
        field.find(".epfl_accordion_section_content").each(function() {
            $(this).children().each(function() {
                $(this).click(function() {
                    var content_id = $(this).attr('data-content-id');
                    var ev = widget_obj.make_widget_event("ContentClick", {full_content_id: content_id});
                    epfl.send(ev);
                });
            });
        });
    }

    // determine which section should be opened
    if(params.value) {
        var section_id = this.wid + "_" + params.value;
        var activeSectionIdx = field.find("h3[data-section-id='"+ section_id +"']").index('h3');
    }
    else {
        var activeSectionIdx = 0;
    }

    // initialize jquery-ui accordion widget
    field.accordion({
        active: activeSectionIdx,
        activate: click_handler,
        heightStyle: "content",
        header: "h3"
    });

    // show field after jquery-ui initialization to prevent ugly elements in the meantime
    field.show();

    // scroll to active element in case the parent has overflow-y and position relative
    try {
        var activeSectionTop = parseInt(field.find("h3[aria-selected='true']").position().top);
        field.scrollTop(activeSectionTop);
    } catch(e) {}
};

epfl.AccordionWidget.inherits_from(epfl.WidgetBase);

epfl.AccordionWidget.prototype.get_value = function() {
    return $("#" + this.wid + " h3[aria-selected='true']").attr("data-section-id");
};
