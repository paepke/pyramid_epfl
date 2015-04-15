import base64

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

    def get_as_binary(self):
        value = str(self.value)
        info, coded_string = str.split(value, ',')
        return base64.b64decode(coded_string)