epfl.paginated_list_goto_complete = function () {
	// remove search indicator, if present
	if ($('#' + '{{ compo.cid }}_search').next().prop("tagName") == "SPAN") {
		$('#' + '{{ compo.cid }}_search').next().remove();
		$('#' + '{{ compo.cid }}_search').parent().removeClass("has-feedback");
	}
}
epfl.paginated_list_goto = function (element, cid, row_offset, row_limit, row_data) {
    if ($(element).hasClass('disabled')) {
        return;
    }
    epfl.set_component_info(cid, 'callback_send_event', 'set_row', epfl.paginated_list_goto_complete);
    epfl.dispatch_event(
    	cid,
    	'set_row',
		{
            row_offset: row_offset,
            row_limit: row_limit,
            row_data: row_data
        });
};


var search_{{ compo.cid }}_timeout;
var search_{{ compo.cid }} = $('#' + '{{ compo.cid }}_search');
search_{{ compo.cid }}
    .keypress(function (e) {
        var elm = this;

        function submit() {
        	if ($(elm).next().prop("tagName") != "SPAN") {
	        	$(elm)
					.after($("<span></span>")
						.addClass("form-control-feedback fa fa-spin fa-spinner")
						.css("margin-right", "15px")
					);
				$(elm)
					.parent()
					.addClass("has-feedback");
			}
			
            var row_data = {search: $(elm).val()};

            if ($("#{{ compo.cid }}_orderby").length && $("#{{ compo.cid }}_ordertype").length) {
                row_data.orderby = $("#{{ compo.cid }}_orderby option:selected").val();
                row_data.ordertype = $("#{{ compo.cid }}_ordertype option:selected").val();
            }
			epfl.paginated_list_goto($(elm),
            "{{ compo.cid }}",
            parseInt({{ compo.row_offset }}),
            parseInt({{ compo.row_limit }}),
            row_data);
            
        }

        if (e.key == 'Enter') {
            submit();
            return;
        }
        if (search_{{ compo.cid }}_timeout) {
            clearTimeout(search_{{ compo.cid }}_timeout);
        }
        search_{{ compo.cid }}_timeout = window.setTimeout(submit, 500);
    });
if (search_{{ compo.cid }}.length > 0) {
    search_{{ compo.cid }}
        .focus()[0]
        .setSelectionRange(search_{{ compo.cid }}.val().length, search_{{ compo.cid }}.val().length);
}
