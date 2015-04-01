
epfl.LoadingComponent = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    epfl.dispatch_event(cid,"check_for_data",{});
};

epfl.LoadingComponent.inherits_from(epfl.ComponentBase);

epfl.LoadingComponent.CheckForData = function(cid,interval){
    setTimeout(function(){
        epfl.dispatch_event(cid,"check_for_data",{});
    },parseInt(interval));
};
