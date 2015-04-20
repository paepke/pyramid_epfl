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

    js_parts = FormInputBase.js_parts + ['upload/upload.js']

    js_name = FormInputBase.js_name + [("solute.epfl.components:upload/static", "upload.js")]

    template_name = "upload/upload.html"

    #: Set true to hide the preview image for the uploaded file.
    no_preview = False

    #: The width of the preview image (if any).
    preview_width = 200

    #: The type of validator that will be used for this field.
    validation_type = 'text'

    fire_change_immediately = True

    def handle_change(self, value):
        self.value = value
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

    def __init__(self, page, cid, label=None, name=None, default="", validation_type="", **extra_params):
        """Download component.

        :param label: Optional label describing the input field.
        :param name: An element without a name cannot have a value.
        :param default: Default value that may be pre-set or pre-selected
        :param validation_type: The type of validator that will be used for this field
        """
        super(Upload, self).__init__(page, cid, label, name, default, validation_type)
