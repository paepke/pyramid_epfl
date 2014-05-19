
epfl.CKEditorWidget = function(wid, cid, params) {
    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    CKEDITOR.replace(params["name"], params["opts"]);

    var ckeditor = CKEDITOR.instances[wid];

    ckeditor.on("instanceReady", function() {
    });

    ckeditor.on("change", function() {
        widget_obj.notify_value_change.call(widget_obj);            
    });



}
epfl.CKEditorWidget.inherits_from(epfl.WidgetBase);

epfl.CKEditorWidget.prototype.get_value = function() {
    var ckeditor = CKEDITOR.instances[this.wid];
    return ckeditor.getData();
};



