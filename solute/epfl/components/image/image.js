$(function () {
epfl.init_component("{{compo.cid}}", "ImageComponent", {"opts": {
                                                        	show_dominant_color: {{ compo.show_dominant_color|format_bool }},
                                                        	show_additional_colors: {{ compo.show_additional_colors|format_bool }}
                                                 		} });
});