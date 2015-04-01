# coding: utf-8

from solute.epfl.core.epflcomponentbase import ComponentBase


class Loading(ComponentBase):
    """
    Loading Component displays an loading indicator as long as the data_loaded function is false
    then the component replace it self with the replace_compo
    """

    asset_spec = "solute.epfl.components:loading/static"
    template_name = "loading/loading.html"
    js_name = ["loading.js"]
    css_name = ["loading.css"]
    js_parts = ["loading/loading.js"]

    compo_state = ["loading_text","check_for_data_interval"]

    compo_config = []

    check_for_data_interval = 1000 #: Recheck interval(milliseconds) in this interval the data_loaded function is called
    replace_compo = None #: the component which got inserted if loading is finish, pass an instance not a class
    loading_text = None #: text which got displayed while loading
    loading_icon = None #: loading icon this will be the full class tag example: 'fa fa-spinner fa-spin fa-5x'
    loading_icon_color = None #: the color of the loading indication use bootstrap classes linke primary danger success etc...


    def handle_check_for_data(self):
        if self.data_loaded():
            self.container_compo.add_component(self.replace_compo)
            self.delete_component()
            self.container_compo.redraw()
        else:
            self.add_js_response("epfl.LoadingComponent.CheckForData('%s',%i)" % (self.cid, self.check_for_data_interval))

    def data_loaded(self):
        # overwrite me
        return True

