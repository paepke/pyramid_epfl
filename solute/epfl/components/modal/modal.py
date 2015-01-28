# coding: utf-8
from solute.epfl.core import epflcomponentbase



class Modal(epflcomponentbase.ComponentContainerBase):

    template_name = "modal/modal.html"
    
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["modal/modal.js"]

    asset_spec = "solute.epfl.components:modal/static"

    js_name = []
    css_name = ["bootstrap.min.css"]

    compo_state = ["title","save_button"]

    compo_config = []

    title = ""
    save_button = False


    def handle_save(self):
        #Overwrite for save handling
        pass

    def open(self):
        self.add_ajax_response("$('#"+self.cid+"_modal').modal('show');")

    def close(self):
        self.add_ajax_response("$('#"+self.cid+"_modal').modal('hide');")






