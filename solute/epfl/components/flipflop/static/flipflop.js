epfl.FlipFlopComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    
    var widget_obj = this;

    var children = $("#"+cid).children();

    $("#" + cid).click(function(event){
        var ev = widget_obj.make_event("onClickChildren",{"compo_id":event.target.id});
        epfl.send(ev); 
    });

};
epfl.FlipFlopComponent.inherits_from(epfl.ComponentBase);

epfl.FlipFlopComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.FlipFlopComponent.prototype.remove_row = function(rowid) {
    console.log("remove",rowid);
    console.log(this.cid);
    $("#" + this.cid + " #" + rowid).remove();
};

