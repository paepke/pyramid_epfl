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

$('#' + '{{ compo.cid }}_search').keypress(function (e) {
    if (e.key == 'Enter') {
        epfl.paginated_list_goto($(this),
                                 "{{ compo.cid }}",
                                 parseInt({{ compo.row_offset }}),
                                 parseInt({{ compo.row_limit }}),
                                 {search: $(this).val()});
    }
});