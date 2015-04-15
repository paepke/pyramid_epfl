epfl.Sortable = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;
    var element = $("#" + cid);
    element.sortable({
        update: function(event, ui){
            var children = element.children("li");
            var newOrder = [];
            for(var i in children){
                if(children[i].id){
                   newOrder.push(children[i].id);
                }
            }
            epfl.dispatch_event(cid, "orderChanged", {"newOrder": newOrder});
        }
    });
	epfl.dispatch_event(cid, "loadingFinished", {});
}; 
epfl.Sortable.inherits_from(epfl.ComponentBase);

epfl.Sortable.prototype.makeSortOrder = function(sort_order){
    var parent = $("li#"+sort_order[0]).parent();
    var elements = [];
    for(var i in sort_order){
        elements.push($("li#"+sort_order[i]).detach());
    }
    for(var i in elements){
        elements[i].appendTo(parent);
    }
}
