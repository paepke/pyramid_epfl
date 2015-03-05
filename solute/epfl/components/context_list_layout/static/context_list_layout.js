epfl.ContextListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    epfl.ContextListLayout.ContextEvent = function (event, param) {
        epfl.dispatch_event(cid, event, param);
    };


    $.fn.epflContextDropDown = function () {
        //init visuals
        $(this).parent().prepend("<button class='btn btn-default btn-xs pull-right'><i class='fa fa-bars'></i></button>");
        $(this).parent().find("button").hide();

        //events
        $(this).children("li.entry").click(function () {
            $(this).parent().hide();
            var liEvent = $(this).data("event");
            var liId = $(this).data("id");
            var liData = $(this).data("data");
            epfl.dispatch_event(cid, liEvent, {entry_id: liId, data: liData});
        });

        $(this).parent().find("button").click(function () {
            var ul = $(this).parent().find("ul");
            if (ul.is(":visible")) {
                ul.hide();
            } else {
                ul.show();
                ul.css({
                    top: ($(this).offset().top + $(this).height() + 3) - $(window).scrollTop(),
                    left: $(this).offset().left
                })
            }
        });

        $($(this).parent()).mouseenter(function () {
            $(this).find("button").show();
        }).mouseleave(function () {
            $(this).find("button").hide();
            $(this).find("ul").hide();
        });
        return this;
    };
    $("#" + cid + " ul.context-dropdown-menu").epflContextDropDown();
};

epfl.ContextListLayout.inherits_from(epfl.ComponentBase);
