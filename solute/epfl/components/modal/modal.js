epfl.ModalComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);


    $('#'+cid+'_modal_save').click(function(){
        epfl.dispatch_event(cid, 'save', {});
    });
};
epfl.ModalComponent.inherits_from(epfl.ComponentBase);

epfl.init_component("{{compo.cid}}" , "ModalComponent", {});