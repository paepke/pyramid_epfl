$(function () {
	 epfl.init_component("{{compo.cid}}"
                      , "FormInputBase",
                      { "submit_form_on_enter": {{ compo.submit_form_on_enter|format_bool }},
                      	"input_focus": {{ compo.input_focus|format_bool }} });
});
