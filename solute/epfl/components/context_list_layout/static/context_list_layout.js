epfl.ContextListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    epfl.ContextListLayout.ContextEvent = function (event, param) {
        epfl.dispatch_event(cid, event, param);
    };

    var epflContextDropDown = function (element) {
        $(this).parent().find("button").hide();

        element.children("li.entry").click(function () {
            $(this).parent().hide();
            var liEvent = $(this).data("event");
            var liId = $(this).data("id");
            var liData = $(this).data("data");
            epfl.dispatch_event(cid, liEvent, {entry_id: liId, data: liData});
        });

        element.parent().find("button").click(function (event) {
            event.stopPropagation();
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
    };
    $(document).click(function(){
        $("#" + cid + " ul.context-dropdown-menu").hide();
    });

    epflContextDropDown($("#" + cid + " ul.context-dropdown-menu"));
};

epfl.ContextListLayout.inherits_from(epfl.ComponentBase);
