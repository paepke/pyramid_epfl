
function get_typeahead(cid, query, process) {
    // TODO: fire event and query results from server
    return ['Amsterdam', 'Washington', 'Sydney', 'Beijing', 'Cairo'];
}

var selector = "#{{compo.cid}}";
console.log($(selector));
var type = $(selector).closest("div").attr('epfl-type');

if (type == "defaultinput" || type == "textarea" || type == "select") {
    $(selector).change(function () {
        epfl.repeat_enqueue(epfl.make_component_event("{{ compo.cid }}", 'change', {value: $(this).val()}), "{{ compo.cid }}");
    });

    provide_typeahead = $(selector).data("provide");
    if (provide_typeahead == "typeahead") {
        $(selector).typeahead({
            source: function (query, process) {
                return process(get_typeahead("{compo.cid}}", query));
            }
        });
    }

} else if (type == "checkbox") {
    $(selector).attr('checked', $("#{{compo.cid}}").val() == 'True');
    $(selector).change(function () {
        var val = val = $(this).is(':checked');
        epfl.repeat_enqueue(epfl.make_component_event("{{ compo.cid }}", 'change', {value: val}), "{{ compo.cid }}");
    });

} else if (type == "toggle") {
    $(selector).attr('checked', $("#{{compo.cid}}").val() == 'True');
    $(selector).bootstrapSwitch('state');
        $(selector).on('switchChange.bootstrapSwitch', function(event, state) {
            var val = $(this).closest("div").parent().hasClass("bootstrap-switch-on");
            epfl.repeat_enqueue(epfl.make_component_event("{{ compo.cid }}", 'change', {value: val}), "{{ compo.cid }}");
        });

} else if (type == "radiobuttongroup") {
    selector = "input[type=radio][name={{ compo.cid }}]";
    $(selector).change(function () {
        var val = val = $(this).is(':checked');
        epfl.repeat_enqueue(epfl.make_component_event("{{ compo.cid }}", 'change', {value: val}), "{{ compo.cid }}");
    });

} else if (type == "buttonsetgroup") {
    selector = "input[type=radio][name={{ compo.cid }}]";
    $(selector).change(function () {
        var val = val = $(this).is(':checked');
        var parent = $(this).parent().parent();
        $(parent).find("label").removeClass("active");
        $(this).parent().addClass("active");
        epfl.repeat_enqueue(epfl.make_component_event("{{ compo.cid }}", 'change', {value: val}), "{{ compo.cid }}");
    });

}

