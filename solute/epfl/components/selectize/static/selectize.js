epfl.Selectize = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);

    var searchServerSide = params["search_server_side"];
    var inputSearchText = params["search_text"];
    var inputFocus = params["input_focus"];
    var cursorPosition = params["cursor_position"];
    var selectedText = params["selected_text"];

    /**************************************************************************
     Helper
     *************************************************************************/
    epfl.Selectize.isVisible = function (cid) {
        return $("#selectize-" + cid + ":visible").length !== 0;
    };

    epfl.Selectize.resetText = function (ele) {
        ele.html(ele.text());
    };

    epfl.Selectize.hide = function (cid) {
        $("#selectize-" + cid).hide();
    };

    epfl.Selectize.show = function (cid) {
        $("#selectize-" + cid).show();
        $("#selectize-" + cid).css({"min-width": $("#selectize-input-" + cid).parent().parent().width() + "px"});
    };

    epfl.Selectize.toggle = function (cid) {
        if (epfl.Selectize.isVisible(cid)) {
            epfl.Selectize.hide(cid);
        } else {
            epfl.Selectize.show(cid);
        }
    };

    /**************************************************************************
     Text decoraction
     using the mark tag bootstrap has css classes for highlighting
     *************************************************************************/
    epfl.Selectize.markText = function (ele, search) {
        var text = ele.text();
        var textlower = text.toLowerCase();
        var searchlower = search.toLowerCase();
        var part1 = text.substr(0, textlower.indexOf(searchlower));
        var searchpart = text.substr(textlower.indexOf(searchlower), search.length);
        var part2 = text.substr(textlower.indexOf(searchlower) + search.length);
        ele.html(part1 + "<mark>" + searchpart + "</mark>" + part2);
    };

    /**************************************************************************
     Resets the list, remove all classes and show everything
     *************************************************************************/
    epfl.Selectize.resetList = function (list) {
        list.find("li").each(function () {
            $(this).find("span").each(function () {
                epfl.Selectize.resetText($(this));
            });

            $(this).parent().parent().next("li.epfl-selectize-divider").show();
            $(this).show();
            $(this).removeClass("selected");
        });
    };


    /**************************************************************************
     Input Events
     *************************************************************************/
    epfl.Selectize.inputOnEnter = function (event) {
        var current = $("li.epfl-selectize.selected:visible").find("li.epfl-selectize.selected:visible");
        if (current.length) {
            epfl.Selectize.resetList($("ul.epfl-selectize"));
            $("#selectize-input-" + cid).val(current.text().trim());
            epfl.Selectize.hide(cid);
            epfl.dispatch_event(cid, "set_selection", {
                selection_id: current.data('selectizeid'),
                selection_value: current.text().trim(),
                selection_group_id: current.closest("li.epfl-selectize-head").find("span").first().data("selectize-groupid"),
                selection_group_value: current.closest("li.epfl-selectize-head").find("span").first().text()
            });
        }
    };

    epfl.Selectize.inputArrowUp = function (event) {
        event.preventDefault();

        //check if something is selected
        if ($(".epfl-selectize.selected:visible").length > 0) {
            //select prev visible if last do nothing
            var current = $("li.epfl-selectize-entry.selected:visible");
            if (current.prev("li:visible").length > 0) {
                current.removeClass("selected");
                current.prev("li:visible").addClass("selected");
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
    };

    epfl.Selectize.inputArrowDown = function (event) {
        event.preventDefault();
        if (!epfl.Selectize.isVisible(cid)) {
            epfl.Selectize.show(cid);
        }

        //check if something is selected
        if ($(".epfl-selectize.selected:visible").length > 0) {
            //select next visible if last do nothing
            var current = $("li.epfl-selectize-entry.selected:visible");
            if (current.next("li:visible").length > 0) {
                current.removeClass("selected");
                current.next("li:visible").addClass("selected");
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
    };

    epfl.Selectize.inputTextChanged = function (searchText) {
        if (searchText.length > 0) {
            epfl.Selectize.show(cid);
        }

        $(".epfl-selectize-head").each(function () {
            epfl.Selectize.resetText($(this).find("span.epfl-selectize-heading"));

            if ($(this).find("span.epfl-selectize-heading").text().toLowerCase().indexOf(searchText.toLowerCase()) === -1) {
                //not found check siblings
                var found = false;

                $(this).find(".epfl-selectize-entry").each(function () {
                    epfl.Selectize.resetText($(this).find("span"));

                    var foundInSibling = $(this).find("span").text().toLowerCase().indexOf(searchText.toLowerCase())

                    if (foundInSibling === -1) {
                        $(this).hide();
                        $(this).parent().parent().next("li.epfl-selectize-divider").hide();
                    } else {
                        $(this).show();
                        $(this).parent().parent().next("li.epfl-selectize-divider").show();
                        epfl.Selectize.markText($(this).find("span"), searchText);
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
                $(this).next("li.epfl-selectize-divider").show();
                $(this).find(".epfl-selectize-entry").each(function () {
                    epfl.Selectize.resetText($(this).find("span"));
                    $(this).show();
                });
                epfl.Selectize.markText($(this).find("span.epfl-selectize-heading"), searchText);
            }
        });
    };

    /**************************************************************************
     Event Listener
     *************************************************************************/
    var search_timeout = null;
    $("#selectize-input-" + cid).keyup(function (event) {
        if (event.which === 13) { // enter
            epfl.Selectize.inputOnEnter(event);
        } else if (event.which === 38) { //arrow up
            epfl.Selectize.inputArrowUp(event);
        } else if (event.which === 40) { //arrow down
            epfl.Selectize.inputArrowDown(event);
        } else {
            if (inputSearchText !== $("#selectize-input-" + cid).val()) {
                inputSearchText = $("#selectize-input-" + cid).val();
                clearTimeout(search_timeout);
                search_timeout = setTimeout(function () {
                    var search = $("#selectize-input-" + cid).val();
                    var cursorPos = $("#selectize-input-" + cid)[0].selectionStart;
                    if (searchServerSide) {
                        epfl.dispatch_event(cid, "update_search", {search_text: search, cursor_position: cursorPos});
                    } else {
                        epfl.Selectize.inputTextChanged(search);
                    }
                }, 500);
            }
        }
    });

    $("#selectize-toggle-" + cid).click(function () {
        $("#selectize-input-" + cid).focus();
        epfl.Selectize.toggle(cid);
    });


    $(".epfl-selectize-entry." + cid).click(function () {
        epfl.Selectize.resetList($("ul.epfl-selectize"));
        $("#selectize-input-" + cid).val($(this).text().trim());
        epfl.Selectize.hide(cid);

        epfl.dispatch_event(cid, "set_selection", {
            selection_id: $(this).data('selectizeid'),
            selection_value: $(this).text().trim(),
            selection_group_id: $(this).closest("li.epfl-selectize-head").find("span").first().data("selectize-groupid"),
            selection_group_value: $(this).closest("li.epfl-selectize-head").find("span").first().text()
        });
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

    /**************************************************************************
     Search Server Side
     if the search server side flag is true every input change triggers the backend to reload the entries
     with this a mechanism you get a pagination style component
     *************************************************************************/
    if (searchServerSide === true && inputSearchText != "") {
        if (selectedText === null) {
            $("#selectize-input-" + cid).val(inputSearchText);
            epfl.Selectize.inputTextChanged(inputSearchText);
        }

    }

    /**************************************************************************
     Width correction
     this is required because you cant inherit the width when your html tag is position fixed
     and Focus
     *************************************************************************/
    $('#' + cid + ' > ul').width($('#' + cid).width());

    if (inputFocus) {
        $("#selectize-input-" + cid).focus();
        var searchTextLength = $("#selectize-input-" + cid).val().length;
        $("#selectize-input-" + cid)[0].setSelectionRange(parseInt(cursorPosition), parseInt(cursorPosition));
    }

};

epfl.Selectize.inherits_from(epfl.ComponentBase);
