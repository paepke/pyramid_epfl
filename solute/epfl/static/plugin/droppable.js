/*
    Epfl Plugin Wrapper for jqueryui droppable
    the element with the selector gets droppable
    the python class behind the cid must implement a handle_drop function
    def handle_drop(self,epflId,text):
        pass
 */

epfl.PluginDroppable = function (selector, cid) {

    $(selector).droppable({
        tolerance: "pointer",
        drop: function (event, ui) {
            var dragEpflId = ui.draggable.attr("epflid");
            var dragText = ui.draggable.text();
            epfl.dispatch_event(cid,"drop",{epflId:dragEpflId,text:dragText});
        }
    });
}