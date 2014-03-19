# -*- coding: utf-8 -*-

from solute.epfl.core import epflwidgetbase

class ImageSelectorWidget(epflwidgetbase.WidgetBase):


    """ A widget which displays a list/row of images to be selected.
    The domain consists of dicts with the following keys:

        id: The unique id of this element (will be passed back as value to the field if the picture is selected)
        name: optional. The name-tag (creates a small tooltip on the image)
        preview_img_src: optional. The URL to the image which will be displayed
        info: optional. A string which will be displayed below the image

    """

    name = "image_selector"
    template_name = "image_selector/image_selector.html"
    asset_spec = "solute.epfl.widgets:image_selector/static"

    js_name = ["image_selector.js"]
    css_name = ["image_selector.css"]

    param_def = {"domain": epflwidgetbase.DomainType,
                 "on_click": epflwidgetbase.EventType, # The name of the event or "submit" to submit the form
                 "default_image_src" : epflwidgetbase.OptionalStringType
                 }

    default_image_src = "/img/p.gif"

    def __init__(self, domain = None, on_click = None, default_image_src = None):

        if not domain:
            domain = []

        super(ImageSelectorWidget, self).__init__(domain=domain,
                                                  on_click=on_click,
                                                  default_image_src=default_image_src)


    def pre_render(self):
        """ Modify and prepare the domain to be used in the jinja-template
        """
        super(ImageSelectorWidget, self).pre_render()

        default_image_src = self.state["params"].get("default_image_src")
        if not default_image_src:
            default_image_src = self.default_image_src

        value = self.field.data
        for item in self.get_domain(f):
            item["name"] = item.get("name", "") # defaulting name to ""
            item["preview_img_src"] = item.get("preview_img_src", default_image_src) # defaulting preview_img_src to ""

            if value is None:
                item["selected"] = False
            elif item["id"] == value:
                item["selected"] = True
            else:
                item["selected"] = False

        if self.get_domain():
            got_domain = True
        else:
            got_domain = False

        self.field.domain_not_empty = got_domain



    def get_selected_domain(self):
        """ Returns the complete item from the domain which corresponds to the selected image.
        IOW: Searches throu the domain-list and returns the item where "id" equals the current value
        """

        id = self.field.data

        domain = self.get_domain()
        for item in domain:
            if item["id"] == id:
                return item

    def get_domain(self):
        """ Returns the complete domain-list """
        domain = self.state["params"]["domain"]
        return domain

