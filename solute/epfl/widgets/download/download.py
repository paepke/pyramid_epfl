# -*- coding: utf-8 -*-


from solute.epfl.core import epflwidgetbase, epflfieldbase


class DownloadWidget(epflwidgetbase.WidgetBase):

    name = "download"
    template_name = "download/download.html"
    asset_spec = "solute.epfl.widgets:download/static"

    js_name = ["download.js"]
    css_name = []

    param_def = {"get_data": epflwidgetbase.MethodType}


    @classmethod
    def add_pyramid_routes(cls, config):
        super(DownloadWidget, cls).add_pyramid_routes(config)

        def download_data(request):
            data = "BLUBBER"
            return Response(status = "200 OK",
                            body = data,
                            content_type = str(fuob.mime_type))


        config.add_route(name = "epfl/widgets/download/data", pattern = '/epfl/download/data/{tid}/{cid}/{wid}')
        config.add_view(download_data, route_name = "epfl/widgets/download/data")



    def handle_onDownload(self):
        data = self.params["get_data"]()
        self.form.return_ajax_response(data)

class Download(epflfieldbase.FieldBase):
    widget_class = DownloadWidget

