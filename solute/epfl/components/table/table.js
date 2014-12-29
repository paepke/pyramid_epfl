 epfl.init_component("{{compo.cid}}", "TableComponent",

                                             {"opts": {
                                                        url: "{{compo.table_data_url}}",
                                                        page: {{compo.current_page}},
                                                        colModel: {{compo.columns_def|tojson}},
                                                        rowNum: "{{compo.num_rows or "Alle"}}",
                                                        rowList: {{compo.num_rows_domain|tojson}},
                                                        pager: "{{compo.cid}}_pager",
                                                        sortname: "{{ compo.sort_column|tojson_ifjson }}",
                                                        sortname_default: "{{compo.sort_column_default}}",
                                                        sortorder: "{{compo.sort_order}}",
                                                        sortorder_default: "{{compo.sort_order_default}}",
                                                        caption: {{compo.caption|tojson}},
                                                        autowidth: {{compo.autowidth|tojson}},
                                                        width: {{compo.width}},
                                                        height: {{compo.height}},
                                                        repeatitems: true,
                                                        gridview: true,
                                                        hiddengrid: !{{compo.table_shown|tojson}},
                                                        keyIndex: "{{compo.index_column_name}}",
                                                        pgtext: {{compo.pager_template|tojson}},
                                                        multisort: {{ compo.multisort|format_bool }}
                                                    },

                                              "scroll_pos": {{compo.scroll_pos|tojson}},
                                              "on_row_click": {{compo.on_row_click|tojson}}

    });