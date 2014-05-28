
epfl.UploadWidget = function(wid, cid, params) {
    var widget_obj = this;

    epfl.WidgetBase.call(this, wid, cid, params);

    $('#' + this.wid).fileupload({
        dataType: 'json',
        formData: function() {
            var ev = widget_obj.make_event("Upload", {});
            return [{ name: "widget_name", value: ev["p"]["widget_name"] },
                    { name: "id", value: ev["id"] }, 
                    { name: "t", value: "upl" }, 
                    { name: "cid", value: ev["cid"] },
                    { name: "tid", value: epfl.tid }]
        },
        done: function (e, data) {
            var url = data.result["preview_url"];
            $("#" + widget_obj.wid + "_preview").html("<a target=\"_blank\" href=\"" + url + "\"><img src=\"" + url + "\" width=\"300\"></a>");
            epfl.show_fading_message("txt_upload_file_ok", "ok");            
        },
        fail: function (e, data) {
            epfl.show_fading_message("txt_upload_file_error", "error");            
        }
    });

}
epfl.UploadWidget.inherits_from(epfl.WidgetBase);

