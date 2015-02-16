# coding: utf-8
from solute.epfl.core import epflcomponentbase



class Modal(epflcomponentbase.ComponentContainerBase):
    """
    Modal Dialog uses the bootstrap modal

    example: http://getbootstrap.com/javascript/#modals

    This is a container compo so set the components you want to display inside in the node_list of the modal
    """

    template_name = "modal/modal.html"
    
    js_parts = epflcomponentbase.ComponentBase.js_parts + ["modal/modal.js"]

    asset_spec = "solute.epfl.components:modal/static"

    js_name = []
    css_name = ["bootstrap.min.css"]

    compo_state = ["title","save_button"]

    compo_config = []

    title = "" #: the title in the modal
    save_button = False #: display save button
    small_modal = False #: display as small modal


    def handle_save(self):
        """
        Overwrite for save handling
        Is called on save button click
        """
        pass

    def open(self):
        self.add_ajax_response("$('#"+self.cid+"_modal').modal('show');")

    def close(self):
        self.add_ajax_response("$('#"+self.cid+"_modal').modal('hide');")

    def handle_close(self):
        """
        Overwrite for close handling
        Is called on close button click
        """
        pass





