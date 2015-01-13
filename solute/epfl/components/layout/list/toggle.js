$('[epflid=' + '{{ compo.cid }}] > i.fa-minus')
    .click(function () {
        epfl.send(epfl.make_component_event('{{ compo.cid }}', 'hide'));
    });

$('[epflid=' + '{{ compo.cid }}] > i.fa-plus')
    .click(function () {
        epfl.send(epfl.make_component_event('{{ compo.cid }}', 'show'));
    });