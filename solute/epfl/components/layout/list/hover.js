{% for compo_obj in compo.components %}
$('[epflid={{ compo_obj.cid }}]').hover(function (e) {
    if (e.type == 'mouseleave') {
        $('#hover_element{{ compo_obj.cid }}').remove();
    } else if (e.type == 'mouseenter') {
        $('<div id="hover_element{{ compo_obj.cid }}">')
            .css('position', 'absolute')
            .css('top', e.pageY + 'px')
            .css('left', e.pageX + 'px')
            .append('<img src="{{ compo_obj.src }}" class="img-thumbnail" />')
            .appendTo(document.body);
    }
});
{% endfor %}