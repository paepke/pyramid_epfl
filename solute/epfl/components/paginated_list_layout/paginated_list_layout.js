epfl.paginated_list_goto_complete = function () {
	// remove search indicator, if present
	if ($('#' + '{{ compo.cid }}_search').next().prop("tagName") == "SPAN") {
		$('#' + '{{ compo.cid }}_search').next().remove();
		$('#' + '{{ compo.cid }}_search').parent().removeClass("has-feedback");
	}
}
epfl.paginated_list_goto = function (element, cid, row_offset, row_limit) {
    if ($(element).hasClass('disabled')) {
        return;
    }
    row_data = {};
    {% if compo.row_data is defined and compo.row_data is mapping %}
    {% for key, value in compo.row_data.iteritems() %}
	    {% if value is number %}
	    	row_data.{{ key }} = {{ value }};
	    {% elif value is string %}
	    	row_data.{{ key }} = '{{ value }}';
	     {% endif %}
	{% endfor %}
    {% endif %}
    row_data.orderby = '{{ compo.row_data['orderby'] if compo.row_data is defined
                                                         and compo.row_data is mapping
                                                         and compo.row_data['orderby'] is defined else '' }}';
    row_data.ordertype = '{{ compo.row_data['ordertype'] if compo.row_data is defined
                                                         and compo.row_data is mapping
                                                         and compo.row_data['ordertype'] is defined else '' }}';
    if($(element) && $(element).hasClass("epfl-search-input")) {
        row_data.search = element.val();
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
    .keyup(function (e) {
        var elm = this;

        function submit() {
            var lastValue = "{{ compo.row_data['search'] if compo.row_data is defined
                                                and compo.row_data is mapping
                                                and compo.row_data['search'] is defined else '' }}";
            if($(elm).val() == lastValue) {
                return;
            }

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
            console.log("!! {{compo.row_data}}");
            var row_data = {{compo.row_data |tojson|safe }};
            row_data.search = $(elm).val();

            if ($("#{{ compo.cid }}_orderby").length && $("#{{ compo.cid }}_ordertype").length) {
                row_data.orderby = $("#{{ compo.cid }}_orderby option:selected").val();
                row_data.ordertype = $("#{{ compo.cid }}_ordertype option:selected").val();
            }
			epfl.paginated_list_goto(elm,
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
 {% if compo.seach_focus is defined and compo.seach_focus == True %}
if (search_{{ compo.cid }}.length > 0) {

    search_{{ compo.cid }}
        .focus()[0]
        .setSelectionRange(search_{{ compo.cid }}.val().length, search_{{ compo.cid }}.val().length);
}

{% endif %}