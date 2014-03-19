# -*- coding: utf-8 -*-

import string
from solute.epfl.core import epflwidgetbase

class CKEditorWidget(epflwidgetbase.WidgetBase):

    """ Integrates the HTML-WYSIWYG-Editor CKEditor: http://ckeditor.com/

    """

    name = "ckeditor"
    template_name = "ckeditor/ckeditor.html"
    asset_spec = "solute.epfl.widgets:ckeditor/static"

    js_name = ["ckeditor/ckeditor.js", "ckeditor.js"]
    css_name = ""

    param_def = {"opts": dict} # the "opts" param contains all configuration for the editor:
    # the following keys are allowed:
    #
    # insert_images: True         Enables/Disables image-handling
    # insert_link: True           Enables/Disables link-handling
    # show_elements_path: False   Enables/Disables the status-line with the html-elements-path from the current cursor position
    # cut_and_paste: True
    # spellcheck: True
    # insert_tables: True
    # insert_hr: True
    # insert_special: True
    # show_source: True
    # style: True
    # format: True
    # maximize: True

    # heights and width of the editor can be passed as kwarg-call-parameter in the jinja-template


    def update_data_source(self, data_source):

        opts = data_source.params["opts"]
        remove_plugins = ["about"]
        remove_buttons = []
        editor_opts = {"language": "de",
                       "removePlugins": ""}

        if not opts.get("insert_images", True):
            remove_plugins.append("image")
        if not opts.get("insert_links", True):
            remove_plugins.append("link")
        if not opts.get("show_elements_path", False):
            remove_plugins.append("elementspath")
            editor_opts["resize_enabled"] = False
        if not opts.get("cut_and_paste", True):
            remove_buttons.extend(["Cut","Copy","Paste","PasteText","PasteFromWord","Undo","Redo"])
        if not opts.get("spellcheck", False):
            remove_buttons.append("SpellChecker")
            remove_plugins.append("scayt")
        if not opts.get("insert_tables", True):
            remove_buttons.append("Table")
            remove_plugins.extend(["table", "tabletools"])
        if not opts.get("insert_hr", True):
            remove_buttons.append("HorizontalRule")
        if not opts.get("insert_special", True):
            remove_buttons.append("SpecialChar")
        if not opts.get("show_source", True):
            remove_buttons.append("Source")
        if not opts.get("maximize", True):
            remove_buttons.append("Maximize")
        if not opts.get("style", True):
            remove_buttons.append("Styles")
        if not opts.get("format", True):
            remove_buttons.append("Format")

        editor_opts["removePlugins"] = string.join(remove_plugins, ",")
        editor_opts["removeButtons"] = string.join(remove_buttons, ",")

        if "width" in data_source.kwargs:
            editor_opts["width"] = data_source.kwargs["width"]

        if "height" in data_source.kwargs:
            editor_opts["height"] = data_source.kwargs["height"]

        data_source.editor_opts = editor_opts

        if not data_source.value:
            data_source.value = u""


