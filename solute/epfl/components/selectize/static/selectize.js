epfl.Selectize = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var searchServerSide = this.params["search_server_side"];
    var inputSearchText = this.params["search_text"];
    var inputFocus = this.params["input_focus"];
    var cursorPosition = this.params["cursor_position"];
    var selectedText = this.params["selected_text"];
    var selectizeInput = $("#selectize-input-" + cid);

    /**************************************************************************
     Event Listener
     *************************************************************************/
    $(".epfl-selectize-entry").hover(function () {
        $(this).addClass("selected").parent().parent().addClass("selected");
    }, function () {
        $(this).removeClass("selected").parent().parent().removeClass("selected");
    });

    $(".epfl-selectize-head").hover(function () {
        $(this).addClass("selected");
    }, function () {
        $(this).removeClass("selected");
    });

    /**************************************************************************
     Search Server Side
     if the search server side flag is true every input change triggers the backend to reload the entries
     with this a mechanism you get a pagination style component
     *************************************************************************/
    if (searchServerSide === true && inputSearchText != "") {
        if (selectedText === null) {
            selectizeInput.val(inputSearchText);
            epfl.Selectize.inputTextChanged(cid, inputSearchText);
        }

    }
    /**************************************************************************
     Width correction
     this is required because you cant inherit the width when your html tag is position fixed
     and Focus
     *************************************************************************/
    $('#' + cid + ' > ul').width($('#' + cid).width());
    if (inputFocus) {
        selectizeInput.focus();
        var searchTextLength = selectizeInput.val().length;
        selectizeInput[0].setSelectionRange(parseInt(cursorPosition), parseInt(cursorPosition));
    }
};

epfl.Selectize.inherits_from(epfl.ComponentBase);

/**************************************************************************
 EPFL New Style Event Handler
 listener are automatically registered
 *************************************************************************/
epfl.Selectize.prototype.handle_click = function (event) {
    epfl.ComponentBase.prototype.handle_click.call(this, event);
    var target = $(event.target);
    var obj = this;

    //click on the drop down button
    if (target.attr("id") === "selectize-toggle-" + obj.cid) {
        $("#selectize-input-" + obj.cid).focus();
        epfl.Selectize.toggle(obj.cid);
    }

    //click on an entry
    if ((target.hasClass("epfl-selectize-entry") && target.hasClass(obj.cid)) ||
            (target.prop("tagName") === "SPAN" && target.hasClass("epfl-selectize") && target.hasClass("epfl-selectize-text"))) {
        epfl.Selectize.resetList($("ul.epfl-selectize"));
        $("#selectize-input-" + obj.cid).val(target.text().trim());
        epfl.Selectize.hide(obj.cid);

        var data = {
            selection_id: target.data('selectizeid'),
            selection_value: target.text().trim(),
            selection_group_id: target.closest("li.epfl-selectize-head").find("span").first().data("selectize-groupid"),
            selection_group_value: target.closest("li.epfl-selectize-head").find("span").first().text()
        };

        if (data.selection_id === undefined) {
            data.selection_id = target.parent().data('selectizeid');
        }

        epfl.dispatch_event(obj.cid, "set_selection", data);
    }
};

epfl.Selectize.prototype.handle_keyup = function (event) {
    epfl.ComponentBase.prototype.handle_keyup.call(this, event);
    var target = $(event.target);
    var obj = this;

    var search_timeout = null;
    var inputSearchText = this.params["search_text"];
    var searchServerSide = this.params["search_server_side"];
    var searchInputElement = $("#selectize-input-" + obj.cid);
    if (target.attr("id") === "selectize-input-" + obj.cid) {
        if (event.which === 13) { // enter
            epfl.Selectize.inputOnEnter(obj.cid, event);
        } else if (event.which === 38) { //arrow up
            epfl.Selectize.inputArrowUp(obj.cid, event);
        } else if (event.which === 40) { //arrow down
            epfl.Selectize.inputArrowDown(obj.cid, event);
        } else { //all other keys: start search after timeout
            if (inputSearchText !== searchInputElement.val()) {
                inputSearchText = searchInputElement.val();
                clearTimeout(search_timeout);
                search_timeout = setTimeout(function () {
                    var search = searchInputElement.val();
                    var cursorPos = searchInputElement[0].selectionStart;
                    if (searchServerSide) {
                        searchInputElement.prop("disabled", true);
                        epfl.dispatch_event(obj.cid, "update_search", {
                            search_text: search,
                            cursor_position: cursorPos
                        });
                    } else {
                        epfl.Selectize.inputTextChanged(obj.cid, search);
                    }
                }, 500);
            }
        }
    }
};

/*************************************************************************
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
    $("#selectize-" + cid).show().css({"min-width": $("#selectize-input-" + cid).parent().parent().width() + "px"});
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

        $(this).removeClass("selected").show().parent().parent().next("li.epfl-selectize-divider").show();
    });
};

/**************************************************************************
 Input Events
 *************************************************************************/
epfl.Selectize.inputOnEnter = function (cid, event) {
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

epfl.Selectize.inputArrowUp = function (cid, event) {
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
        $("li.epfl-selectize:visible").first().addClass("selected")
                .first().find("li.epfl-selectize:visible").first().addClass("selected");
    }
};

epfl.Selectize.inputArrowDown = function (cid, event) {
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
        $("li.epfl-selectize:visible").first().addClass("selected")
                .first().find("li.epfl-selectize:visible").first().addClass("selected");
    }
};

epfl.Selectize.inputTextChanged = function (cid, searchText) {
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
                    $(this).hide().parent().parent().next("li.epfl-selectize-divider").hide();
                } else {
                    $(this).show().parent().parent().next("li.epfl-selectize-divider").show();
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
            $(this).show().next("li.epfl-selectize-divider").show().find(".epfl-selectize-entry").each(function () {
                epfl.Selectize.resetText($(this).find("span"));
                $(this).show();
            });
            epfl.Selectize.markText($(this).find("span.epfl-selectize-heading"), searchText);
        }
    });
};

