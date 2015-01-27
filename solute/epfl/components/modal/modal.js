/**
 * Created by mast on 27.01.15.
 */



epfl.ModalComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    $('#'+cid+'_modal').modal()
};
epfl.ModalComponent.inherits_from(epfl.ComponentBase);

epfl.ModalComponent.prototype.fire_event = function(event_name, params, callback_fn) {
    if (!params) {
        params = {}
    };
    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.init_component("{{compo.cid}}" , "ModalComponent", {});