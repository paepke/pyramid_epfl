/**
 * Created by mast on 06.02.15.
 */
epfl.Simpletree = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);



    var selector = "#" + cid;
    var dataAreaSelector = selector + " div.epfl-simple-tree-data";

    //If the tree data are loading don't make any js stuff
    if($(dataAreaSelector).length === 0){
        return;
    }

    /**************************************************************************
     Helper
     *************************************************************************/
    var get_parent_leafid = function (element) {
        if (element.hasClass("epfl-simple-tree-leaf-2")) {
            return String(element.prevAll(".epfl-simple-tree-leaf-1").first().data("leafid"));
        } else if (element.hasClass("epfl-simple-tree-leaf-1")) {
            return String(element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid"));
        }
        return null;
    };

    //Get the leafids from all upper leafs element is a jquery object
    var get_leafids = function (element) {
        var result = {
            level_0: null,
            level_1: null,
            level_2: null,
            level_3: null,
            level: null
        };

        if (element.hasClass("epfl-simple-tree-leaf-0")) {
            result.level = 0;
            result.level_0 = String(element.data("leafid"));

        } else if (element.hasClass("epfl-simple-tree-leaf-1")) {
            result.level = 1;
            result.level_0 = String(element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid"));
            result.level_1 = String(element.data("leafid"));

        } else if (element.hasClass("epfl-simple-tree-leaf-2")) {
            result.level = 2;
            result.level_0 = String(element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid"));
            result.level_1 = String(element.prevAll(".epfl-simple-tree-leaf-1").first().data("leafid"));
            result.level_2 = String(element.data("leafid"));
        } else if (element.hasClass("epfl-simple-tree-leaf-3")) {
            result.level = 3;
            result.level_0 = String(element.prevAll(".epfl-simple-tree-leaf-0").first().data("leafid"));
            result.level_1 = String(element.prevAll(".epfl-simple-tree-leaf-1").first().data("leafid"));
            result.level_2 = String(element.prevAll(".epfl-simple-tree-leaf-2").first().data("leafid"));
            result.level_3 = String(element.data("leafid"));
        }
        return result;
    };


    /**************************************************************************
     Scroll
     We need the hidden scroll area for scrolling when an element is dragging
     the user can move to the upper or lower area of the tree which then scrolls
     *************************************************************************/
	
	// Remember scroll position
	$(dataAreaSelector).scroll(function () {
        clearTimeout($.data(this, 'simpletree_scrolltimer'));
        $.data(this, 'simpletree_scrolltimer', setTimeout(function () { // detect scroll stop
            epfl.enqueue(epfl.make_component_event(cid, "scrolled", {scroll_position: $(dataAreaSelector).scrollTop()}));
        }, 250));
    });

    //When the tree reloads go back to the last scroll position stored in transaction
    $(dataAreaSelector).scrollTop(params["scroll_position"]);

    //Sets the positon of the scrollarea
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

    //The scroll function of the hidden scroll area
    var scrollUpMouseOver = false;
    $(selector + " div.epfl-simple-tree-scroll-upper").droppable({
        tolerance: "pointer",
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
        tolerance: "pointer",
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
     Tree Leaf Events
     *************************************************************************/

    $(selector + " div.epfl-simple-tree-leaf-0 span i:first-child").click(function (event) {
    	event.stopPropagation();
        var open = $(this).data("open");
        if (open) {
            epfl.dispatch_event(cid, "leaf_0_close", {
                leafid: String($(this).data("leafid"))
            });
        } else {
            epfl.dispatch_event(cid, "leaf_0_open", {
                leafid: String($(this).data("leafid")),
                hover: false
            });
        }
    });

    epfl.Simpletree.Leaf1OpenClose = function (leafid, parent_id, open, thiscid) {
        if (open) {
            epfl.dispatch_event(thiscid, "leaf_1_close", {
                leafid: leafid, level_0_id: parent_id
            });
        } else {
            epfl.dispatch_event(thiscid, "leaf_1_open", {
                leafid: leafid, level_0_id: parent_id,
                hover: false
            });
        }
    };
    
    epfl.Simpletree.Leaf2OpenClose = function (leafid, level_1_id, level_0_id, open, thiscid) {
        if (open) {
            epfl.dispatch_event(thiscid, "leaf_2_close", {
                leafid: leafid, level_1_id: level_1_id, level_0_id: level_0_id
            });
        } else {
            epfl.dispatch_event(thiscid, "leaf_2_open", {
                leafid: leafid, level_1_id: level_1_id, level_0_id: level_0_id,
                hover: false
            });
        }
    };

    epfl.Simpletree.Leaf0Click = function (leafid, open, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_0_clicked", {
            leafid: leafid, leaf_open: open
        });
    };

    epfl.Simpletree.Leaf1Click = function (leafid, level_0_id, open, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_1_clicked", {
            leafid: leafid, level_0_id: level_0_id, leaf_open: open
        });
    };

    epfl.Simpletree.Leaf2Click = function (leafid, level_1_id, level_0_id, open, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_2_clicked", {
            leafid: leafid, level_1_id: level_1_id,
            level_0_id: level_0_id, leaf_open: open
        });
    };
    
    epfl.Simpletree.Leaf3Click = function (leafid, level_2_id, level_1_id, level_0_id, open, thiscid) {
        epfl.dispatch_event(thiscid, "leaf_3_clicked", {
            leafid: leafid, level_2_id: level_2_id, level_1_id: level_1_id,
            level_0_id: level_0_id, leaf_open: open
        });
    };


    
    /**************************************************************************
     Drag and Drop
     window.epflSimpleTreeDragging is required for mouseover effects while dragging an element
     the effects are setting classes for ui highlighting and send event for tree leaf open
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
                drag_level_3: drag_leafids.level_3,
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
                    leafid: String($(that).data("leafid")),
                    hover: true
                });
            } else if ($(that).hasClass("epfl-simple-tree-leaf-1")) {
                var parent_id = get_parent_leafid($(that));
                epfl.dispatch_event(cid, "leaf_1_open", {
                    leafid: String($(that).data("leafid")),
                    level_0_id: parent_id,
                    hover: true
                });
            } else if ($(that).hasClass("epfl-simple-tree-leaf-2")) {
				parent_leaf_ids = get_leafids($(that));
                epfl.dispatch_event(cid, "leaf_2_open", {
                    leafid: String($(that).data("leafid")),
                    level_1_id: parent_leaf_ids.level_1,
                    level_0_id: parent_leaf_ids.level_0,
                    hover: true
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

//This function is triggered from init_transaction for loading the tree data 'async' which means you first see the
//loading indicator on the tree and when the data are loaded they got shown via a epfl redraw
epfl.Simpletree.LoadData = function(cid){
    epfl.enqueue(epfl.make_component_event(cid, 'load_data', {}), cid);
    setTimeout(function(){
        epfl.flush();
        $('#epfl_please_wait').hide();
    },100);
};

