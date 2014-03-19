
epfl.init_ckeditor_widget = function(params) {
	$(document).ready(function() {
		CKEDITOR.replace(params["name"], params["opts"]);
	});
};
