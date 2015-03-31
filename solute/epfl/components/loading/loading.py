# coding: utf-8

from solute.epfl.core.epflcomponentbase import ComponentBase


class Loading(ComponentBase):
    """
    Simple Badge Compo uses bootstrap badge

    example: http://getbootstrap.com/components/#badges
    """

    template_name = "loading/loading.html"

    asset_spec = "solute.epfl.components:loading/static"
    js_name = ["loading.js"]

    css_name = ["loading.css"]

    js_parts = ["loading/loading.js"]

    compo_state = ["replace_compo","loading_text"]

    compo_config = []

    check_for_data_interval = 1000

    replace_compo = None

    loading_text = None

    def handle_check_for_data(self):
        if self.data_loaded():
            self.container_compo.replace_component(self,self.replace_compo)
        else:
            self.add_js_response("epfl.LoadingComponent.CheckForData('%s',%i)" % (self.cid, self.check_for_data_interval))

    def data_loaded(self):
        # overwrite me
        return True

