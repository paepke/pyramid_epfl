/**
 * Created by mast on 06.02.15.
 */
epfl.Simpletree = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    $("div[epflid='" + cid + "'] input.epfl-simple-tree-search").change(function () {
        epfl.dispatch_event(cid, "search", {search: $(this).val()});
    });

    $("div.epfl-simple-tree-leaf-0").click(function () {
        epfl.dispatch_event(cid, "leaf_0_clicked", {leafid: $(this).attr("leafid")});
    });

    epfl.Simpletree.Leaf1Clicked = function (leafid) {
        epfl.dispatch_event(cid, "leaf_1_clicked", {leafid: leafid});
    };

    var dragables = $("div[epflid='" + cid + "'] div.epfl-simple-tree-leaf-dragable");
    dragables.draggable({
        revert: true,
        containment: 'window',
        scroll: false,
        helper: 'clone',
        cursorAt: { top: 0, left: 0 }
    });
};

epfl.Simpletree.inherits_from(epfl.ComponentBase);

