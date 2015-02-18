epfl.TextEditor = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
	var compo = this;
    var selector = "#" + cid;

    var editor = CKEDITOR.replace(cid);
    editor.on('change', function (evt) {
        epfl.repeat_enqueue(epfl.make_component_event(cid, 'change', {value:  evt.editor.getData()}), cid);
    });
}; 
epfl.TextEditor.inherits_from(epfl.ComponentBase);

