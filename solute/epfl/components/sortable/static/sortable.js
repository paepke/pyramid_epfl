epfl.SortableComponent = function(cid, params) {
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
            var ev = compo.make_event("orderChanged",{"newOrder":newOrder});
            epfl.send(ev);
        }
    });

    epfl.send(compo.make_event("loadingFinished",{}));
}; 
epfl.SortableComponent.inherits_from(epfl.ComponentBase);

epfl.SortableComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) { params = {} };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};


epfl.SortableComponent.prototype.makeSortOrder = function(sort_order){
    var parent = $("li#"+sort_order[0]).parent();
    var elements = [];
    for(var i in sort_order){
        elements.push($("li#"+sort_order[i]).detach());
    }
    for(var i in elements){
        elements[i].appendTo(parent);
    }
}
