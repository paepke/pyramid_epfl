$('[epflid=' + '{{ compo.cid }}] > .tree-label.expanded')
    .click(function () {
        epfl.send(epfl.make_component_event('{{ compo.cid }}', 'hide'));
    });

$('[epflid=' + '{{ compo.cid }}] > .tree-label.collapsed')
    .click(function () {
        epfl.send(epfl.make_component_event('{{ compo.cid }}', 'show'));
    });
