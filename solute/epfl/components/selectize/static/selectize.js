epfl.Selectize = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    $("[epflid='"+cid+"'] > ul").width($("[epflid='"+cid+"']").width());

    epfl.Selectize.isVisible = function (cid) {
        return $("#selectize-" + cid + ":visible").length !== 0;
    }

    epfl.Selectize.resetText = function (ele) {
        ele.html(ele.text());
    }

    epfl.Selectize.show = function (cid) {
        $("#selectize-" + cid).show();
        $("#selectize-" + cid).css({"min-width":$("#selectize-input-" + cid).parent().parent().width()+"px"});
    }

    epfl.Selectize.hide = function (cid) {
        $("#selectize-" + cid).hide();
    }

    epfl.Selectize.toggle = function (cid) {
        if (epfl.Selectize.isVisible(cid)) {
            epfl.Selectize.hide(cid);
        } else {
            epfl.Selectize.show(cid);
        }
    }

    epfl.Selectize.markText = function (ele, search) {
        var text = ele.text();
        var textlower = text.toLowerCase();
        var searchlower = search.toLowerCase();
        var part1 = text.substr(0, textlower.indexOf(searchlower));
        var searchpart = text.substr(textlower.indexOf(searchlower), search.length);
        var part2 = text.substr(textlower.indexOf(searchlower) + search.length);
        ele.html(part1 + "<mark>" + searchpart + "</mark>" + part2);
    }

    epfl.Selectize.resetList = function (list) {
        list.find("li").each(function () {
            $(this).find("span").each(function () {
                epfl.Selectize.resetText($(this));
            });
            $(this).show();
            $(this).removeClass("selected");
        });
    }


    $("#selectize-toggle-" + cid).click(function () {
        $("#selectize-input-" + cid).focus();
        epfl.Selectize.toggle(cid);
    });

    $("#selectize-input-" + cid).keyup(function (event) {
        if (event.which === 13) {
            var current = $("li.epfl-selectize.selected:visible").find("li.epfl-selectize.selected:visible");
            if (current.length) {
                epfl.Selectize.resetList($("ul.epfl-selectize"));
                $("#selectize-input-" + cid).val(current.text().trim());
                epfl.Selectize.hide(cid);
                epfl.dispatch_event(cid, "set_selection", {selection_id: current.data('selectizeid'), selection_text: current.text().trim()});
            }
            return;
        }
        else if (event.which === 38) { //arrow up
            event.preventDefault();


            //check if something is selected
            if ($(".epfl-selectize.selected:visible").length > 0) {
                //select prev visible if last do nothing
                var current = $("li.epfl-selectize.selected:visible").find("li.epfl-selectize.selected:visible");
                if (current.prev("li").length > 0) {
                    current.removeClass("selected");
                    current.prev("li").addClass("selected");
                } else {
                    var prevSelectize = $("li.epfl-selectize.selected:visible").prev().prev();
                    if (prevSelectize.length > 0) {
                        current.removeClass("selected");
                        current.parent().parent().removeClass("selected");
                        prevSelectize.addClass("selected");
                        prevSelectize.find("li.epfl-selectize:visible").last().addClass("selected");
                    }
                }
            } else {
                //select first visible
                $("li.epfl-selectize:visible").first().addClass("selected");
                $("li.epfl-selectize:visible").first().find("li.epfl-selectize:visible").first().addClass("selected");
            }


            return;
        } else if (event.which === 40) { //arrow down
            event.preventDefault();
            if (!epfl.Selectize.isVisible(cid)) {
                epfl.Selectize.show(cid);
            }

            //check if something is selected
            if ($(".epfl-selectize.selected:visible").length > 0) {
                //select next visible if last do nothing
                var current = $("li.epfl-selectize.selected:visible").find("li.epfl-selectize.selected:visible");

                if (current.next("li").length > 0) {
                    current.removeClass("selected");
                    current.next("li").addClass("selected");
                } else {
                    var nextSelectize = $("li.epfl-selectize.selected:visible").next().next();
                    if (nextSelectize.length > 0) {
                        current.removeClass("selected");
                        current.parent().parent().removeClass("selected");
                        nextSelectize.addClass("selected");
                        nextSelectize.find("li.epfl-selectize:visible").first().addClass("selected");
                    }
                }
            } else {
                //select first visible
                $("li.epfl-selectize:visible").first().addClass("selected");
                $("li.epfl-selectize:visible").first().find("li.epfl-selectize:visible").first().addClass("selected");
            }

            return;
        }

        var search = $("#selectize-input-" + cid).val();
        if (search.length > 0) {
            epfl.Selectize.show(cid);
        }

        $(".epfl-selectize-head").each(function () {
            epfl.Selectize.resetText($(this).find("span.epfl-selectize-heading"));

            if ($(this).find("span.epfl-selectize-heading").text().toLowerCase().indexOf(search.toLowerCase()) === -1) {
                //not found check siblings
                var found = false;

                $(this).find(".epfl-selectize-entry").each(function () {
                    epfl.Selectize.resetText($(this).find("span"));

                    var foundInSibling = $(this).find("span").text().toLowerCase().indexOf(search.toLowerCase())

                    if (foundInSibling === -1) {
                        $(this).hide();
                    } else {
                        $(this).show();
                        epfl.Selectize.markText($(this).find("span"), search);
                        found = true;
                    }
                });

                if (found) {
                    $(this).show();
                } else {
                    $(this).hide();
                }
            } else {
                //found show all
                $(this).show();
                $(this).find(".epfl-selectize-entry").each(function () {
                    epfl.Selectize.resetText($(this).find("span"));
                    $(this).show();
                });
                epfl.Selectize.markText($(this).find("span.epfl-selectize-heading"), search);
            }
        });
    });

    $(".epfl-selectize-entry." + cid).click(function () {
        epfl.Selectize.resetList($("ul.epfl-selectize"));
        $("#selectize-input-" + cid).val($(this).text().trim());
        epfl.Selectize.hide(cid);
        epfl.dispatch_event(cid, "set_selection", {selection_id: $(this).data('selectizeid'), selection_text: $(this).text().trim()});
    }).mouseenter(function () {
        $(this).addClass("selected");
        $(this).parent().parent().addClass("selected");
    }).mouseleave(function () {
        $(this).removeClass("selected");
        $(this).parent().parent().removeClass("selected");
    });

    $(".epfl-selectize-head").mouseenter(function () {
        $(this).addClass("selected");
    }).mouseleave(function () {
        $(this).removeClass("selected");
    });
};

epfl.Selectize.inherits_from(epfl.ComponentBase);


