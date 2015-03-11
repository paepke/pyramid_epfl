/**
 * Created by mast on 06.02.15.
 */
epfl.Simpletree = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    $("#" + cid + " input.epfl-simple-tree-search").change(function () {
        epfl.dispatch_event(cid, "search", {
            search_string: $(this).val(),
            filter_key: $("#" + cid + " select.epfl-simple-tree-filter").val()
        });
    });

    $("#" + cid + " button.epfl-simple-tree-search-btn").click(function () {
        epfl.dispatch_event(cid, "search", {
            search_string: $(this).val(),
            filter_key: $("#" + cid + " select.epfl-simple-tree-filter").val()
        });
    });


    $("#" + cid + " select.epfl-simple-tree-filter").change(function () {
        epfl.dispatch_event(cid, "search", {
            search_string: $("#" + cid + " input.epfl-simple-tree-search").val(),
            filter_key: $(this).val()
        });
    });

    $("#" + cid + " div.epfl-simple-tree-leaf-0").click(function () {
        epfl.dispatch_event(cid, "leaf_0_clicked", {leafid: $(this).attr("leafid")});
    });

    epfl.Simpletree.Leaf1Clicked = function (leafid,parent_id, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_1_clicked", {leafid: leafid,parent_id:parent_id});
    };
    epfl.Simpletree.Leaf2Clicked = function (leafid, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_2_clicked", {leafid: leafid});
    };

    var dragables = $("#" + cid + " div.epfl-simple-tree-leaf-dragable");
    dragables.draggable({
        revert: "invalid",
        scroll: false,
        helper: 'clone',
        cursorAt: {top: 10, left: 10}
    });

    var droppables = $("#" + cid + " div.epfl-simple-tree-leaf-droppable");

    droppables.droppable({
        accept: ".epfl-simple-tree-leaf-dragable",
        hoverClass: "epfl-simple-tree-leaf-droppable-hover",
        drop: function (event, ui) {

            var get_parent_leafid = function (element) {
                if (element.hasClass("epfl-simple-tree-leaf-2")) {
                    return element.prevAll("epfl-simple-tree-leaf-1").first().attr("leafid");
                } else if (element.hasClass("epfl-simple-tree-leaf-1")) {
                    return element.prevAll("epfl-simple-tree-leaf-0").first().attr("leafid");
                }
                return null;
            }

            var drag_parent_leafid = get_parent_leafid(ui.draggable);
            var drop_parent_leafid = get_parent_leafid($(this));
            console.log("drag_parent_leafid",drag_parent_leafid,"drop_parent_leafid",drop_parent_leafid);
            epfl.dispatch_event(cid, "drop", {
                drag_leafid: ui.draggable.attr("leafid"),
                drag_parent_leafid: drag_parent_leafid,
                drag_tree_cid: ui.draggable.closest("div[epflid]").attr('epflid'),
                drop_leafid: $(this).attr("leafid"),
                drop_parent_leafid: drop_parent_leafid,
                drop_tree_cid: $(this).closest("div[epflid]").attr('epflid')
            });
        }
    });

    epfl.Simpletree.ContextEvent = function (event, param) {
        epfl.dispatch_event(cid, event, param);
    };

    $("#" + cid + " button.epfl-simple-tree-dropdown-button").click(function (event) {
        event.stopPropagation();
        var parent = $(this).parent();
        if (parent.hasClass('open')) {
            parent.removeClass("open");
        } else {
            parent.addClass("open");
        }
        var posi = $(this).offset();

        var ul = $(this).next("ul");
        var top = posi.top - 3;
        var left = posi.left + $(this).width() + 10;
        var menuEnterd = false;

        if (left + ul.width() > $(window).width()) {
            left = posi.left - (ul.width() + 3)
        }

        ul.css({
            top: top - $(window).scrollTop(),
            left: left,
            position: "fixed"
        });
        $(this).parent().mouseleave(function () {
            $(this).removeClass("open");
            $(this).unbind("mouseleave");
        });

        $(window).scroll(function () {
            parent.removeClass("open");
            $(this).unbind("scroll");
        });
    });

    $("#" + cid + " ul.epfl-simple-tree-dropdown").mouseleave(function () {
        $(this).dropdown('toggle');
    });

};

epfl.Simpletree.inherits_from(epfl.ComponentBase);

