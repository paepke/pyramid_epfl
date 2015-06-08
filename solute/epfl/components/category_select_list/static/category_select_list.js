epfl.CategorySelectList = function (cid, params) {
    epfl.PaginatedListLayout.call(this, cid, params);
};

epfl.CategorySelectList.inherits_from(epfl.PaginatedListLayout);

epfl.CategorySelectList.prototype.after_response = function (data) {
    epfl.PaginatedListLayout.prototype.after_response.call(this, data);
    var obj = this;

    var searchText = obj.elm.find("#" + obj.cid + "_search").val();
    if (searchText.length > 0) {
        obj.show();
        obj.elm.find("#" + obj.cid + "_search").focus();
    }
};

epfl.CategorySelectList.prototype.handle_click = function (event) {
    epfl.PaginatedListLayout.prototype.handle_click.call(this, event);
    var target = $(event.target);
    var obj = this;
    if (target.hasClass("btn")) {
        obj.toggle();
    } else if (target.hasClass("epfl-new-selectize-text")) {
        $("#" + obj.cid + "_search").val(target.text().trim());
        obj.hide(obj.cid);
        var data = {
            selection_id: target.parent().data('selectizeid'),
            selection_value: target.text().trim(),
            selection_group_id: target.closest("li.epfl-new-selectize-head").find("span").first().data("selectize-groupid"),
            selection_group_value: target.closest("li.epfl-new-selectize-head").find("span").first().text()
        };

        epfl.dispatch_event(obj.cid, "set_selection", data);
    }
};

epfl.CategorySelectList.prototype.handle_keyup = function (event) {
    epfl.PaginatedListLayout.prototype.handle_keyup.call(this, event);
    var target = $(event.target);
    var obj = this;
    var searchText = obj.elm.find("#" + obj.cid + "_search").val();


    if (target.attr("id") === obj.cid + "_search" && obj.isVisible()) {
        if (event.which === 13) { // enter
            var selected = obj.elm.find("li.epfl-new-selectize-entry.selected");
            if (selected.length) {
                $("#" + obj.cid + "_search").val(target.text().trim());
                obj.hide(obj.cid);
                var data = {
                    selection_id: selected.data('selectizeid'),
                    selection_value: selected.children().first().text().trim(),
                    selection_group_id: selected.closest("li.epfl-new-selectize-head").find("span").first().data("selectize-groupid"),
                    selection_group_value: selected.closest("li.epfl-new-selectize-head").find("span").first().text()
                };
                epfl.dispatch_event(obj.cid, "set_selection", data);
            }

        } else if (event.which === 38 || event.which === 40) { //arrow up //arrow down
            var entries = obj.elm.find("li.epfl-new-selectize-entry");
            if (entries.length !== 0) {
                var selectedIndex = null;
                for (var i = 0; i < entries.length; i++) {
                    if ($(entries[i]).hasClass("selected")) {
                        selectedIndex = i;
                        break;
                    }
                }
                if (selectedIndex === null) {
                    $(entries[0]).addClass("selected");
                } else {
                    if (event.which === 40) {//down
                        if (selectedIndex !== entries.length - 1) {
                            $(entries[selectedIndex]).removeClass("selected");
                            $(entries[selectedIndex + 1]).addClass("selected");
                        }
                    } else if (event.which === 38) {//up
                        if (selectedIndex !== 0) {
                            $(entries[selectedIndex]).removeClass("selected");
                            $(entries[selectedIndex - 1]).addClass("selected");
                        }
                    }

                }
            }
        }
    }
};


epfl.CategorySelectList.prototype.isVisible = function () {
    return $("#selectize-" + this.cid + ":visible").length !== 0;
};

epfl.CategorySelectList.prototype.hide = function () {
    $("#selectize-" + this.cid).hide();
};

epfl.CategorySelectList.prototype.show = function () {
    $("#selectize-" + this.cid).show().css({"min-width": $("input.epfl-search-input").parent().parent().width() + "px"});
};

epfl.CategorySelectList.prototype.toggle = function () {
    if (this.isVisible()) {
        this.hide();
    } else {
        this.show();
    }
};