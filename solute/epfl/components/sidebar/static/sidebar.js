epfl.Sidebar = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    $("#"+cid+ " ul.epfl-sidebar-navi li.epfl-sidebar-navi-entry").mouseenter(function(){
        $(this).children("ul.epfl-sidebar-menu").show();
    }).mouseleave(function(){
        $(this).children("ul.epfl-sidebar-menu").hide();
    });

    $("#"+cid+ " li.epfl-sidebar-menu-entry").click(function(){
        epfl.dispatch_event(cid,"go_to_page",{url:$(this).data("url"),parent_name:$(this).data("parent-name")});
    });
};

epfl.Sidebar.inherits_from(epfl.ComponentBase);


