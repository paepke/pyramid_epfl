epfl.Sidebar = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $("#" + cid + " ul.epfl-sidebar-navi li.epfl-sidebar-navi-entry").mouseenter(function () {
        $(this).children("ul.epfl-sidebar-menu").show();
    }).mouseleave(function () {
        $(this).children("ul.epfl-sidebar-menu").hide();
    });
    
    var setServerModePosition = function () {
        $("#" + cid + " div.epfl-sidebar-servermode").css({
            "position": "fixed",
            "top": $(window).height() - 20
        });
    };
    $(window).resize(setServerModePosition);
    setServerModePosition();
};

epfl.Sidebar.inherits_from(epfl.ComponentBase);


