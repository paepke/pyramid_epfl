epfl.paginated_list_goto = function (element, cid, row_offset, row_limit, row_data) {
    if ($(element).hasClass('disabled')) {
        return;
    }
    var event = epfl.make_component_event(
        cid,
        'set_row',
        {
            row_offset: row_offset,
            row_limit: row_limit,
            row_data: row_data
        });
    epfl.send(event);
};


var {{ compo.cid }}_timeout;
$('#' + '{{ compo.cid }}_search').keypress(function (e) {
    var elm = this;
    function submit() {
        epfl.paginated_list_goto($(elm),
                                 "{{ compo.cid }}",
                                 parseInt({{ compo.row_offset }}),
                                 parseInt({{ compo.row_limit }}),
                                 {search: $(elm).val()});
    }

    if (e.key == 'Enter') {
        submit();
    }
    if ({{ compo.cid }}_timeout) {
        clearTimeout({{ compo.cid }}_timeout);
    }
    {{ compo.cid }}_timeout = window.setTimeout(submit, 500);
});