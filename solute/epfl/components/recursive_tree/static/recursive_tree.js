epfl.RecursiveTree = function(cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var selector = '[epflid=' + cid + ']';

    var compo = this;

    var elm = $(selector);
    var label = $(selector + ' > span');
    var icon = $(selector + ' > i');

    label.click(function () {
        epfl.send(compo.make_event('click_label'));
    });

    icon.click(function () {
        epfl.send(compo.make_event('click_icon'));
    });
};

epfl.RecursiveTree.inherits_from(epfl.ComponentBase);
