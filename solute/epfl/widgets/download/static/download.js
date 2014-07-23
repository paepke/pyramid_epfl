epfl.DownloadWidget = function(wid, cid, params) {
    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);


    $("#" + this.wid).click(function(e) {
        e.preventDefault();

        var ev = widget_obj.make_event("onDownload", {});
        epfl.send(ev);
    });

}


epfl.DownloadWidget.inherits_from(epfl.WidgetBase);