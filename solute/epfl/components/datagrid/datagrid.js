epfl.DataGridComponent = function (cid, params) {
    epfl.ComponentBase.call(this, cid, params);
    var compo = this;

    columns = [];
    {% for field in compo.fields %}
        columns.push({
            field: "{{field.id}}",
            title: "{{field.name}}"
            {% if field.type is defined%}
                {% if field.type == "element" %}
                    ,formatter: "epfl.DataGridComponent.elementFormatter"
                {% endif %}
            {% endif %}
            {% if field.align is defined %}
                ,align : "{{field.align}}"
                ,valign:"{{field.align}}"
            {% endif %}
        });
    {% endfor %}


    $("#datagrid_{{compo.cid}}").bootstrapTable({
        method:"get",
        url:"{{ compo.data_url }}",
        height: {{compo.height}},
        pagination: true,
        sidePagination: "server",
        pageList:  [10, 25, 50, 100, 200],
        search:true,
        columns:columns,
        onLoadSuccess: epfl.DataGridComponent.onLoadSuccess
    });

   epfl.DataGridComponent.buttonFormaterClickHandler = function(eventname){
       var evt = compo.make_event(eventname,{});
       epfl.send(evt);
   }

};

epfl.DataGridComponent.onLoadSuccess = function (data) {
    data.forEach(function (row) {
        for (var key in row) {
            if (!row[key].type) {
                continue;
            }
            if (row[key].type == "diagramm") {
                $("#" + row[key].name).highcharts( {
                        title : { text:null},
                        tooltip:{enabled:false},
                        plotOptions: {
                            pie: {
                                dataLabels: {
                                    enabled: false
                                },
                                showLegend: false
                            }
                        },
                        series: [{
                            type: 'pie',
                            name: 'Browser share',
                            data: [
                                ['Firefox', 45.0],
                                ['IE', 26.8],
                                ['Safari', 8.5],
                                ['Opera', 6.2],
                                ['Others', 0.7]
                            ]
                        }]
                    });
                $("#" + row[key].name).find(".highcharts-button").hide();
                $("#" + row[key].name).find("text").hide();
            }
        }
    });
};

epfl.DataGridComponent.inherits_from(epfl.ComponentBase);

epfl.DataGridComponent.prototype.fire_event = function (event_name, params, callback_fn) {
    if (!params) {
        params = {}
    }

    var evt = this.make_event(event_name, params);
    epfl.send(evt, callback_fn)
};

epfl.init_component("{{compo.cid}}", "DataGridComponent", {});

epfl.DataGridComponent.elementFormatter = function (data, row) {
    if (!data || !data.type) {
        return data;
    }

    if (data.type == "diagramm") {
        return "<div id='"+data.name+"' style='min-width: 100px; height: 100px; max-width: 100px; margin: 0 auto'></div>";
    } else if (data.type == "icon") {
        var size = '1';
        if(data.size){
            size = data.size;
        }
        return '<i class="fa fa-' + data.icon + ' fa-'+ size+'x"></i> ' + data.text;
    } else if (data.type == "button") {
        return "<button type='button' class='btn btn-default' onclick='epfl.DataGridComponent.buttonFormaterClickHandler(\""+ data.handler + "\")'>" + data.text + "</button>";
    }
};



