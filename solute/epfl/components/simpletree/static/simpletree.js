/**
 * Created by mast on 06.02.15.
 */
epfl.Simpletree = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var selector = "#" + cid;
    var dataAreaSelector = selector + " div.epfl-simple-tree-data";

    /**************************************************************************
     Helper
     *************************************************************************/
    var get_parent_leafid = function (element) {
        if (element.hasClass("epfl-simple-tree-leaf-2")) {
            return parseInt(element.prevAll(".epfl-simple-tree-leaf-1").first().data("leafid"));
        } else if (element.hasClass("epfl-simple-tree-leaf-1")) {
            return parseInt(element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid"));
        }
        return null;
    };
    
    var get_leafids = function (element) {
        var result = {
            level_0: null,
            level_1: null,
            level_2: null,
            level: null
        };

        if (element.hasClass("epfl-simple-tree-leaf-0")) {
            result.level = 0;
            result.level_0 = element.data("leafid");

        } else if (element.hasClass("epfl-simple-tree-leaf-1")) {
            result.level = 1;
            result.level_0 = element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid");
            result.level_1 = element.data("leafid");

        } else if (element.hasClass("epfl-simple-tree-leaf-2")) {
            result.level = 2;
            result.level_0 = element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid");
            result.level_1 = element.prevAll(".epfl-simple-tree-leaf-1").first().data("leafid");
            result.level_2 = element.data("leafid");
        }
        return result;
    };


    /**************************************************************************
     Scroll
     *************************************************************************/

    $(dataAreaSelector).scrollTop(params["scrollTop"]);

    var setHiddenScrollArea = function () {
        $(selector + " div.epfl-simple-tree-scroll-upper").css({
            "width": $("#" + cid).width() + "px",
            "top": $(dataAreaSelector).offset().top - $(window).scrollTop(),
            "left": $(dataAreaSelector).offset().left - $(window).scrollLeft()
        });

        $(selector + " div.epfl-simple-tree-scroll-lower").css({
            "width": $("#" + cid).width() + "px",
            "top": ($(dataAreaSelector).offset().top + $(dataAreaSelector).height() - 10) - $(window).scrollTop(),
            "left": $(dataAreaSelector).offset().left - $(window).scrollLeft()
        });
    };
    setHiddenScrollArea();

    $(window).scroll(function () {
        setHiddenScrollArea();
    });

    var scrollUpMouseOver = false;
    $(selector + " div.epfl-simple-tree-scroll-upper").droppable({
        over: function (event, ui) {
            scrollUpMouseOver = true;
            var scrollUp = function () {
                if (scrollUpMouseOver === true) {
                    $(dataAreaSelector).scrollTop($(dataAreaSelector).scrollTop() - 30);
                    setTimeout(scrollUp, 100);
                }
            };
            scrollUp();
        },
        out: function (event, ui) {
            scrollUpMouseOver = false;
        },
        drop: function (event, ui) {
            scrollUpMouseOver = false;
        }
    });

    var scrollDownMouseOver = false;
    $(selector + " div.epfl-simple-tree-scroll-lower").droppable({
        over: function (event, ui) {
            scrollDownMouseOver = true;
            var scrollDown = function () {
                if (scrollDownMouseOver === true) {
                    $(dataAreaSelector).scrollTop($(dataAreaSelector).scrollTop() + 30);
                    setTimeout(scrollDown, 100);
                }
            };
            scrollDown();
        },
        out: function (event, ui) {
            scrollDownMouseOver = false;
        },
        drop: function (event, ui) {
            scrollDownMouseOver = false;
        }
    });

    /**************************************************************************
     Search and Filter
     *************************************************************************/

    $(selector + " input.epfl-simple-tree-search").change(function () {
        epfl.dispatch_event(cid, "search", {
            search_string: $(this).val(),
            filter_key: $(selector + " select.epfl-simple-tree-filter").val()
        });
    });

    $(selector + " button.epfl-simple-tree-search-btn").click(function () {
        epfl.dispatch_event(cid, "search", {
            search_string: $(this).val(),
            filter_key: $(selector + " select.epfl-simple-tree-filter").val()
        });
    });

    $(selector + " select.epfl-simple-tree-filter").change(function () {
        epfl.dispatch_event(cid, "search", {
            search_string: $(selector + " input.epfl-simple-tree-search").val(),
            filter_key: $(this).val()
        });
    });

    /**************************************************************************
     Tree Leaf Events
     *************************************************************************/

    $(selector + " div.epfl-simple-tree-leaf-0").click(function () {
        var open = $(this).data("open");
        if (open) {
            epfl.dispatch_event(cid, "leaf_0_close", {
                leafid: parseInt($(this).data("leafid")),
                scroll_top: $(dataAreaSelector).scrollTop()
            });
        } else {
            epfl.dispatch_event(cid, "leaf_0_open", {
                leafid: parseInt($(this).data("leafid")),
                scroll_top: $(dataAreaSelector).scrollTop()
            });
        }
    });

    epfl.Simpletree.Leaf1Clicked = function (leafid, parent_id, open, thiscid) {
        if (open) {
            epfl.dispatch_event(thiscid, "leaf_1_close", {
                leafid: leafid, parent_id: parent_id,
                scroll_top: $(dataAreaSelector).scrollTop()
            });
        } else {
            epfl.dispatch_event(thiscid, "leaf_1_open", {
                leafid: leafid, parent_id: parent_id,
                scroll_top: $(dataAreaSelector).scrollTop()
            });
        }
    };

    epfl.Simpletree.Leaf2Clicked = function (leafid, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_2_clicked", {
            leafid: leafid,
            scroll_top: $(dataAreaSelector).scrollTop()
        });
    };

    /**************************************************************************
     Drag and Drop
     *************************************************************************/

    $(selector + " div.epfl-simple-tree-leaf-dragable").draggable({
        revert: "invalid",
        scroll: false,
        helper: 'clone',
        cursorAt: {top: -5, left: -5},
        containment: "window",
        zIndex: 5000,
        scroll: true,
        start: function (event, ui) {
            window.epflSimpleTreeDragging = true;
            $(this).addClass("epfl-simple-tree-leaf-dragging");
        },
        stop: function (event, ui) {
            window.epflSimpleTreeDragging = false;
            $(this).removeClass("epfl-simple-tree-leaf-dragging");
        },
        appendTo: "body"
    });

    $(selector + " div.epfl-simple-tree-leaf-droppable").droppable({
        accept: ".epfl-simple-tree-leaf-dragable",
        tolerance: "pointer",
        drop: function (event, ui) {

            var drag_leafids = get_leafids(ui.draggable);
            var drop_leafids = get_leafids($(this));
            epfl.dispatch_event(cid, "drop", {
                drag_level:drag_leafids.level,
                drag_level_0: drag_leafids.level_0,
                drag_level_1: drag_leafids.level_1,
                drag_level_2: drag_leafids.level_2,
                drag_tree_cid: ui.draggable.closest("div[epflid]").attr('epflid'),
                drop_level:drop_leafids.level,
                drop_level_0: drop_leafids.level_0,
                drop_level_1: drop_leafids.level_1,
                drop_level_2: drop_leafids.level_2,
                drop_tree_cid: $(this).closest("div[epflid]").attr('epflid')
            });

        }
    });
    var openTimeout;
    $(selector + " div.epfl-simple-tree-leaf-droppable").mouseenter(function () {
        if (window.epflSimpleTreeDragging === undefined ||
            window.epflSimpleTreeDragging === false) {
            return;
        }

        $(this).addClass("epfl-simple-tree-leaf-droppable-hover");

    }).mouseleave(function () {
        if ($(this).hasClass("epfl-simple-tree-leaf-droppable-hover")) {
            $(this).removeClass("epfl-simple-tree-leaf-droppable-hover");
        }
    });

    $(selector + " div.epfl-simple-tree-openable[data-open='false']").mouseenter(function () {
        if (window.epflSimpleTreeDragging === undefined ||
            window.epflSimpleTreeDragging === false) {
            return;
        }
        var that = this;
        openTimeout = setTimeout(function () {
            if ($(that).hasClass("epfl-simple-tree-leaf-0")) {
                epfl.dispatch_event(cid, "leaf_0_open", {
                    leafid: parseInt($(that).data("leafid")),
                    scroll_top: $(dataAreaSelector).scrollTop()
                });
            } else if ($(that).hasClass("epfl-simple-tree-leaf-1")) {

                var parent_id = get_parent_leafid($(that));
                epfl.dispatch_event(cid, "leaf_1_open", {
                    leafid: parseInt($(that).data("leafid")),
                    parent_id: parseInt(parent_id),
                    scroll_top: $(dataAreaSelector).scrollTop()
                });

            }
        }, 500);
    }).mouseleave(function () {
        clearTimeout(openTimeout);
    });


    /**************************************************************************
     Context Menu
     *************************************************************************/
    epfl.PluginContextMenu(selector + " ul.context-dropdown-menu", cid);
};

epfl.Simpletree.inherits_from(epfl.ComponentBase);

