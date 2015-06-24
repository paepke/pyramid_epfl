import base64
import requests

from solute.epfl.components.form.form import FormInputBase


class Upload(FormInputBase):
    """
    A form upload field.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[Upload(label="Image:", name="image")])
    
    """

    js_name = FormInputBase.js_name + [("solute.epfl.components:upload/static", "upload.js"),
                                       ("solute.epfl.components:upload/static", "jquery.iframe-transport.js"),
                                       ("solute.epfl.components:upload/static", "jquery.fileupload.js")]

    css_name = FormInputBase.css_name + [("solute.epfl.components:upload/static", "upload.css"),]

    template_name = "upload/upload.html"

    compo_state = FormInputBase.compo_state + ["allowed_file_types","show_remove_icon","maximum_file_size"]

    #: Set true to hide the preview image for the uploaded file.
    no_preview = False

    #: The width of the preview image (if any).
    preview_width = 200

    #: The type of validator that will be used for this field.
    validation_type = 'text'

    #: Sends changes immediately
    fire_change_immediately = True

    #: Allowed file types if not allowed nothing happens: give a list with file type endings example: ["png","gif","jpg"]
    allowed_file_types = None

    #: show a remove icon which removes the current uploaded file see: handle_remove_icon
    show_remove_icon = False

    #: maximum file size in byte this is checked in javascript, the hard limit is 200 MB
    maximum_file_size = 5 * 1024 * 1024


    new_style_compo = True
    compo_js_params = ['fire_change_immediately','allowed_file_types','show_remove_icon','maximum_file_size']
    compo_js_name = 'Upload'

    def handle_change(self, value):
        self.value = value
        if self.no_preview is False:
            self.redraw()

    def get_as_binary(self):
        value = self.value
        if str(value).startswith('http') is True:
            # Upload data is from another url, so we have to parse it first
            binary = requests.get(value).content
        else:
            info, coded_string = str.split(str(value), ',')
            binary = base64.b64decode(coded_string)
        return binary

    def handle_remove_icon(self):
        self.value = None
        self.redraw()

    def __init__(self, page, cid, label=None, name=None, default="", validation_type="", **extra_params):
        """Download component.

        :param label: Optional label describing the input field.
        :param name: An element without a name cannot have a value.
        :param default: Default value that may be pre-set or pre-selected
        :param validation_type: The type of validator that will be used for this field
        """
        super(Upload, self).__init__(page, cid, label, name, default, validation_type)
