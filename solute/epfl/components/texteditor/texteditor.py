from solute.epfl.components.form.util import FormInputBase


class TextEditor(FormInputBase):
    """
    A form wysiwyg text editor supporting BBCode.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[TextEditor(label="Provide a description:", name="description")])
    
    """

    js_parts = ['texteditor/texteditor.js']
    js_name = [('solute.epfl.components:texteditor/static', 'texteditor.js')]
    js_name_no_bundle = [('solute.epfl.components:texteditor/static', 'ckeditor.js')]

    template_name = "texteditor/texteditor.html"

    validation_type = 'text'

    #: The config-file that should be used for this instance. Available are at least "config" and "slimconfig"
    editor_config_file = "config"

    #: Set True to automatically remove all formatting on paste
    clean_paste = False
