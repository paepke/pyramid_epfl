import base64
import requests
import ujson as json

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
    js_parts = []

    css_name = FormInputBase.css_name + [("solute.epfl.components:upload/static", "upload.css"), ]

    template_name = "upload/upload.html"

    compo_state = FormInputBase.compo_state + ["allowed_file_types", "show_remove_icon", "maximum_file_size",
                                               "handle_click", "store_async", "height", "width", "file_size",
                                               "file_type"]

    height = None #: Compo height in px if none nothing is set

    width = None #: Compo width in px if none nothing is set

    plus_icon_size = "5x" #: The plus icon in dropzone, use the font awesome sizes 1x - 5x or lg

    #: Set true to hide the preview image for the uploaded file.
    no_preview = False

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

    #: Shows the file input
    show_file_upload_input = True

    #: shows the dropzone
    show_drop_zone = False

    #: Margin of drop zone icon and label in percentage from the upper drop zone border.
    #: Can be adapted in order to yield reasonable layout based on different drop zone icon sizes
    drop_zone_add_position_top = 35

    #: Additional label text shown in the drop zone, if set
    drop_zone_add_text = None

    #: Generate a handle_click event if the component is clicked on by the user.
    handle_click = False

    #: Upload the image immediately via handle_store, store has to return a URI that will be used as value.
    store_async = False

    file_size = None  #: File Size of the current uploaded filed
    file_type = None  #: File Type of the current uploaded filed

    new_style_compo = True
    compo_js_params = ['fire_change_immediately', 'allowed_file_types', 'show_remove_icon', 'maximum_file_size',
                       'value', 'handle_click', 'store_async','show_file_upload_input','show_drop_zone']
    compo_js_extras = ['handle_drop', 'handle_click']
    compo_js_name = 'Upload'

    def __init__(self, page, cid, label=None, name=None, default=None, validation_type=None, handle_click=None,
                 store_async=None, **extra_params):
        """Download component.

        :param label: Optional label describing the input field.
        :param name: An element without a name cannot have a value.
        :param default: Default value that may be pre-set or pre-selected
        :param validation_type: The type of validator that will be used for this field
        :param handle_click: Generate a handle_click event if the component is clicked on by the user.
        :param store_async: Upload the image immediately via handle_store, store has to return a URI that will be used
                            as value.
        """
        super(Upload, self).__init__(page, cid, label, name, default, validation_type)

    def handle_change(self, value):
        """
        When an image gets dropped over the dropzone or an image is choosen in file input
        :param url: image url if the image's source is desktop or epfl image compo url is a byte string
        """
        self.value = value
        if self.no_preview is False:
            self.redraw()

    def handle_store(self, data, file_name):
        self.add_ajax_response(json.encode(self.store(data, file_name)))

    def store(self, data, file_name):
        return data

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

    def handle_drop_accepts(self, cid, moved_cid):
        self.add_ajax_response('true')

    def handle_file_info(self, file_size, file_type):
        self.file_size = file_size
        self.file_type = file_type
        print self.file_size,self.file_type

