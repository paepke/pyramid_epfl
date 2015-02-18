from solute.epfl.components.form.form import FormInputBase


class TextEditor(FormInputBase):
    """
    A form wysiwyg text editor supporting BBCode.
    
    Typically, this component is used in a form:
    
    .. code:: python
        
        form = Form(node_list=[TextEditor(label="Provide a description:", name="description")])
    
    """

    js_parts = ['texteditor/texteditor.js']
    js_name = [('solute.epfl.components:texteditor/static', 'texteditor.js'),
               ('solute.epfl.components:texteditor/static', 'ckeditor.js')]

    template_name = "texteditor/texteditor.html"

    validation_type = 'text'
