# coding: utf-8
from solute.epfl.core import epflcomponentbase,epflutil

from pyramid.response import Response
import json

class DataGrid(epflcomponentbase.ComponentBase):

    template_name = "datagrid/datagrid.html"
    js_parts = "datagrid/datagrid.js"

    asset_spec = "solute.epfl.components:datagrid/static"

    js_name = ["bootstrap-table.js","highcharts.js"]
    css_name = ["datagrid.css","bootstrap.min.css","bootstrap-table.css"]

    compo_state = ["data_url"]

    compo_config = []

    #Overwrite these !
    data_url = ""
    fields = []

    #General Settings
    height = 400
    data_search = True
    card_view = False

    #Pagination Settings
    pagination = True
    page_list = "[5, 10, 20, 50, 100, 200]"
    page_size = 10


    def init_transaction(self):
        cid = self.cid
        tid = self.page.transaction.get_id()
        self.data_url = "/epfl/datagrid/getdata/" + str(tid) + "/" + str(cid)

    def get_data(self,limit,offset,order,search):
        # Overwrite me !
        #
        # limit is the count of data in the current view
        # offset is the position in current data
        # so the data you return are something like data_array[offset : offset + limit]
        # order is order
        # search is the search string
        #
        # return an json parseable dict with total and rows fields
        # total is the total count of all posible data
        # rows are the data visible in the current view
        return {"total": 0, "rows": []}


    @classmethod
    def add_pyramid_routes(cls, config):
        super(DataGrid, cls).add_pyramid_routes(config)

        def get_data(request):
            tid = request.matchdict["tid"]
            cid = request.matchdict["cid"]
            limit = int(request.params.get("limit", 0))
            offset = int(request.params.get("offset", 0))
            order = request.params.get("order", None)
            search = request.params.get("search", None)

            compo = epflutil.get_component_from_root_node(request,tid,cid)
            data = compo.get_data(limit,offset,order,search)

            return Response(json.dumps(data))

        config.add_route(name = 'epfl/components/datagrid/getdata', pattern = '/epfl/datagrid/getdata/{tid}/{cid}')
        config.add_view(get_data, route_name = "epfl/components/datagrid/getdata")

