epfl.ContextListLayout = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    epfl.ContextListLayout.ContextEvent = function (event, param) {
        epfl.dispatch_event(cid, event, param);
    };

    epfl.PluginContextMenu("#" + cid + " ul.context-dropdown-menu",cid);
};

epfl.ContextListLayout.inherits_from(epfl.ComponentBase);
