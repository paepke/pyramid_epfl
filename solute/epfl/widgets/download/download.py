# -*- coding: utf-8 -*-

from pyramid.response import Response
from solute.epfl.core import epflwidgetbase, epflfieldbase, epflutil


class DownloadWidget(epflwidgetbase.WidgetBase):

    name = "download"
    template_name = "download/download.html"
    asset_spec = "solute.epfl.widgets:download/static"

    js_name = ["download.js"]
    css_name = []

    param_def = {"get_data": epflwidgetbase.MethodType} #Defined method must return the dict with "data" and "filename" parameters


    @classmethod
    def add_pyramid_routes(cls, config):
        super(DownloadWidget, cls).add_pyramid_routes(config)

        def download_data(request):
            tid = request.matchdict["tid"]
            cid = request.matchdict["cid"]
            wid = request.matchdict["wid"]

            widget = epflutil.get_widget(request, tid, cid, wid)
            download_data = widget.params["get_data"]()

            return Response(status = "200 OK",
                            body = download_data["data"],
                            content_type = "application/force-download",
                            content_disposition = 'attachment; filename="{filename}"'.format(filename=download_data["filename"]))


        config.add_route(name = "epfl/widgets/download/data", pattern = '/epfl/download/data/{tid}/{cid}/{wid}')
        config.add_view(download_data, route_name = "epfl/widgets/download/data")



    def handle_onDownload(self):
        url=self.request.route_url("epfl/widgets/download/data", tid=self.form.page.transaction.get_id(),
                                                                 cid=self.form.get_component_id(),
                                                                 wid=self.get_wid())

        self.form.page.jump_extern(url, target="_self")
class Download(epflfieldbase.FieldBase):
    widget_class = DownloadWidget

