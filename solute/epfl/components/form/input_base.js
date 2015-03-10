$(function () {
	 epfl.init_component("{{compo.cid}}"
                      , "FormInputBase",
                      { "submit_form_on_enter": {{ compo.submit_form_on_enter|format_bool }},
                      	"input_focus": {{ compo.input_focus|format_bool }},
                      	"fire_change_immediately": {{ compo.fire_change_immediately|format_bool }},
                        "compo_col":{{compo.compo_col}},
                        "label_col":{{compo.label_col}},
                        "vertical":"{{compo.layout_vertical}}"
});
});
