$(function () {
   epfl.init_component("{{compo.cid}}", "TableLayout", {'fixed_header': {{ compo.fixed_header|format_bool }}});
});
