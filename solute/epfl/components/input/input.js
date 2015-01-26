$(function () {
	 epfl.init_component("{{compo.cid}}"
                      , "InputComponent",
                      { "submit_form_on_enter": {{ compo.submit_form_on_enter|format_bool }} });
});
