epfl.ContextListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    epfl.ContextListLayout.ContextEvent = function (event, param) {
        epfl.dispatch_event(cid, event, param);
    };


    $("#" + cid + " button.epfl-context-list-dropdown-button").click(function () {
        var posi = $(this).offset();
        var ul = $(this).next("ul");
        var top = posi.top - 3;
        var left = posi.left + $(this).width() + 15;
        var menuEnterd = false;

        if (left + ul.width() > $(window).width()) {
            left = posi.left - (ul.width() + 3)
        }

        ul.css({
            top: top,
            left: left,
            position: "fixed"
        });
        $(this).parent().mouseleave(function(){
            $(this).removeClass("open");
        });
    });

    $("#" + cid + " ul.epfl-context-list-dropdown").mouseleave(function(){
            $(this).dropdown('toggle');
    });
};

epfl.ContextListLayout.inherits_from(epfl.ComponentBase);
