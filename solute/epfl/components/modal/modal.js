epfl.ModalComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);


    $('#'+cid+'_modal_save').click(function(){
        epfl.dispatch_event(cid, 'save', {});
    });
    $('#'+cid+'_modal_close').click(function(){
        epfl.dispatch_event(cid, 'close', {});
    });
    $('#'+cid).on('shown.bs.modal', function () {
    	$(this).find("input").first().focus();
	});
};
epfl.ModalComponent.inherits_from(epfl.ComponentBase);

epfl.init_component("{{compo.cid}}" , "ModalComponent", {});