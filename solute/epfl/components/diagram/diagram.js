$(function () {
	 epfl.init_component("{{compo.cid}}"
                      , "DiagramComponent",
                      {{ compo.get_params()|tojson }});
});