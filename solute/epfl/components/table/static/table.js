
epfl.TableComponent = function(cid, params) {

    epfl.ComponentBase.call(this, cid, params);

    var compo_obj = this;

    params["opts"]["viewrecords"] = true;

    params["opts"]["onHeaderClick"] = function(gridstate) { compo_obj.on_header_click.call(compo_obj, gridstate) };

    params["opts"]["datatype"] = function(postdata) { compo_obj.data_type_func.call(compo_obj, postdata); };

    // resize column handling
    params["opts"]["resizeStop"] = function(new_width, col_idx) { compo_obj.resize_top_func.call(compo_obj, new_width, col_idx) };

    if (!params["opts"]["pgtext"]) { delete params["opts"]["pgtext"] };

    params["opts"]["onSelectRow"] = function(row_idx) {
        var row_id = compo_obj.get_rowid_by_idx.call(compo_obj, row_idx);
        var ev = epfl.make_component_event(compo_obj.cid, "setTargetRowId", {"row_id": row_id});
        epfl.enqueue(ev);
        if (compo_obj.params["on_row_click"]) {
            var cmd = compo_obj.params["on_row_click"];
            var ev = epfl.make_component_event(compo_obj.cid, cmd, {});
            epfl.send(ev);
        };
    }

    // draw it!
    $("#" + cid + "_table").jqGrid(params["opts"]);

    // scroll-pos handling
    this.table_container_div = $("#" + cid + "_table").closest(".ui-jqgrid-bdiv");
    this.table_container_div.scroll(function() { compo_obj.table_container_div_scrollfn.call(compo_obj) });

};
epfl.TableComponent.inherits_from(epfl.ComponentBase);

epfl.TableComponent.prototype.destroy = function() {
    epfl.ComponentBase.prototype.destroy.call(this);

    var thegrid = $("#" + this.cid + "_table");
    thegrid.GridDestroy();
};


epfl.TableComponent.prototype.table_container_div_scrollfn = function() {

    //BaseClass.prototype.getName.call(this); super class method calling

    if (!this.table_container_div) return;

    var top_pos = this.table_container_div.scrollTop();
    var left_pos = this.table_container_div.scrollLeft();
    this.params["scroll_pos"] = [top_pos, left_pos];
    var ev = this.make_event("setScrollPos", {"top": top_pos,
                                              "left": left_pos});
    epfl.repeat_enqueue(ev, this.cid + "/scroll")
}


epfl.TableComponent.prototype.resize_stop_func = function(new_width, col_idx) {
    var ev = this.make_event("setColumnWidth", {"col_idx": col_idx,
                                                    "new_width": new_width});
    epfl.enqueue(ev);
};

epfl.TableComponent.prototype.data_type_func = function(postdata) {
    if (postdata.rows == "Alle") {
        var num_rows = null;
    }
    else {
        var num_rows = parseInt(postdata.rows);
    }

    if (!postdata.page) {
        var page = 1;
    }
    else {
        var page = parseInt(postdata.page);
    }

    var sort_column = postdata.sidx;
    var sort_order = postdata.sord;

    epfl.show_please_wait();
    if (this.params["opts"]["multisort"]){
        if (typeof sort_column === 'string'){
            var buff = {};
            buff[sort_column] = [sort_order, 0];
            sort_column = buff;
        }
    } else {
        if (sort_column == "None") {
            sort_column = null;
        }
        sort_column = this.colname2idx(sort_column);
    }

    var compo_obj = this;
    var ev = this.make_event("getData", {"num_rows": num_rows,
                                         "page": page,
                                         "sort_column": sort_column,
                                         "sort_order": sort_order});

    epfl.json_request(ev, function(data) {
        var thegrid = $("#" + compo_obj.cid + "_table")[0];
        thegrid.addJSONData(data);

        // register click-events
        $("#" + compo_obj.cid + "_table").find(".epfl_clickevent").each( function() {
            $(this).click(function(event) {
                event.stopPropagation(); // if you click on icons in rows, you get no row-event
                var row_id = compo_obj.get_rowid_by_object.call(compo_obj, this);
                var cmd = $(this).attr("cmd");
                var ev = epfl.make_component_event(compo_obj.cid, "setTargetRowId", {"row_id": row_id});
                epfl.enqueue(ev);
                var ev = epfl.make_component_event(compo_obj.cid, cmd, {});
                epfl.send(ev);

            });
        });

        setTimeout(function() {
            epfl.hide_please_wait();
            var scroll_top = compo_obj.params["scroll_pos"][0];
            var scroll_left = compo_obj.params["scroll_pos"][1];
            compo_obj.table_container_div.scrollTop(scroll_top);
            compo_obj.table_container_div.scrollLeft(scroll_left);
            compo_obj.table_container_div.scroll(compo_obj.table_container_div_scrollfn);
            compo_obj.table_container_div.css({"visibility":""});
        }, 0);
    });
};


epfl.TableComponent.prototype.on_header_click = function(gridstate) {
    var ev = this.make_event("foldTable", {"table_shown": gridstate == "visible"});
    epfl.repeat_enqueue(ev, this.cid + "/fold");
};

epfl.TableComponent.prototype.refresh_data = function() {
    var thegrid = $("#" + this.cid + "_table");
    this.table_container_div.unbind("scroll", this.table_container_div_scrollfn);
    this.table_container_div.css({"visibility":"hidden"});
    thegrid.trigger("reloadGrid");
};

epfl.TableComponent.prototype.colname2idx = function(col_name) {
    for (var idx = 0; idx < this.params.opts.colModel.length; idx++) {
        if (this.params.opts.colModel[idx].name == col_name) {
            return idx;
        };
    };
    return null;
};

epfl.TableComponent.prototype.get_rowid_by_object = function(dom_obj) {
    var thegrid = $("#" + this.cid + "_table");
    var row_id = $(dom_obj).closest("tr").attr("id");
    if (!row_id) return null;
    var row_data = thegrid.jqGrid("getRowData", row_id);
    return row_data[this.params["opts"]["keyIndex"]];
};

epfl.TableComponent.prototype.get_rowid_by_idx = function(idx) {
    var thegrid = $("#" + this.cid + "_table");
    var row_data = thegrid.jqGrid("getRowData", idx);
    return id = row_data[this.params["opts"]["keyIndex"]];
};


// formatters
jQuery.extend($.fn.fmatter, {
    "icon_formatter": function(cellvalue, options, row) {
        var alt_attr = "", lnk_open = "", lnk_close = ""
        if (!cellvalue["src"]) { return ''; }
        if (cellvalue["tip"]) { alt_attr = "alt='" + cellvalue["tip"] + "' title='" + cellvalue["tip"] + "'"; }
        if (cellvalue["link"]) {
            lnk_open = "<a href='" + cellvalue["link"] + "'";
            if (cellvalue["target"]) {
                lnk_open += " target='" + cellvalue["target"] + "'>";
            } else {
                lnk_open += ">";
            }
            lnk_close = "</a>"; }
        if (cellvalue["cmd"]) { lnk_open = "<div class='epfl_clickevent clickable' cmd='" + cellvalue["cmd"] + "'>"; lnk_close = "</div>" }
        return lnk_open + "<img border='0' " + alt_attr + " align='absmiddle' src='" + cellvalue["src"] + "' />" + lnk_close;
    },
    "anchor_formatter": function(cellvalue, options, row) {
        if (!cellvalue["href"]) { return ''; }

        var href_attr = "href='" + cellvalue["href"] + "' ";
        var target_attr = "target='" + cellvalue["target"] + "' ";
        var class_attr = "class='" + cellvalue["class"] + "' ";
        var style_attr = "style='" + cellvalue["style"] + "' ";

        var link = "<a " + href_attr + target_attr + class_attr + style_attr + ">" + cellvalue["name"] + "</a>"

        return link;
    }
});
