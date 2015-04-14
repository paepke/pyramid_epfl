epfl.Loading = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    epfl.dispatch_event(cid,"check_for_data",{});
};

epfl.Loading.inherits_from(epfl.ComponentBase);

epfl.Loading.CheckForData = function(cid,interval){
    setTimeout(function(){
        epfl.dispatch_event(cid,"check_for_data",{});
    },parseInt(interval));
};
