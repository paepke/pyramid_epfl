#* coding: utf-8

import re

from jinja2.exceptions import TemplateNotFound
from pyramid_jinja2 import SmartAssetSpecLoader

class MacroAccessor(object):
    """ Can be used to access the macros inside a template. If the macro is not defined, a nice error will be raised.
    Access the macros in dict-style.
    """

    is_template_element = False # to please the reflection-module

    def __init__(self, template_obj):
        self.template_obj = template_obj


    def __getattr__(self, key):
        """ Access the macro as dict-style-attribute """
        try:
            module = self.template_obj.module
            return getattr(module, key)
        except AttributeError, e:
##            import __svc__
            info = parseAttributeError(e)
            print "DEBUG HINT:"
            print info
            # this dirty trick stores usefull debugging-information in a "global" variable...
##            __svc__.jinja.exception_debug_hint = "Template '%s' has no macro named '%s'" % (self.template_obj.filename, info["missing_attribute"])
            # ... and re-raises the exception to let the jinja-stack rewrite the error-message
            # (this finally calls GlobalJinja._exception_formatter )
            # there is no other way to modify the error-message and keep the jinja-error-rewriting mechanism
            raise

def parseAttributeError(excep):
    """ Parse the message of an AttributeError-Exception.
    """
    tokens = excep.message.split()
    return {"missing_attribute": tokens[-1].strip("'")}


class PreprocessingFileSystemLoader(SmartAssetSpecLoader):

    def crop_compo_definiton(self, template, compo_name):
        """ This one searches the component definition in the template and returns it """

        # find the start:
        mo = re.search(r"\{\%\s*compo\s+" + compo_name + r"\s*\(", template) # search for "{% compo COMPO_NAME("
        if not mo:
            return None

        start_pos = pos = mo.start(0)
        nesting = 0

        # find the end:
        while pos < len(template):
            pos = template.find("{%", pos + 1)
            if pos == -1:
                return None

            tokens = template[pos + 2:pos + 20].split()
            if tokens[0] == "endcompo":
                if nesting == 0:
                    # got it, and it's my {% endcompo %} 
                    # not the one from another compo-def
                    end_pos = template.find("%}", pos) + 2
                    return template[start_pos:end_pos]

                nesting -= 1
            elif tokens[0] == "compo":
                nesting += 1


    def get_source(self, environment, template):

        if "redraw:" in template:
            template, redraw_compo = template.split(" redraw:") # ugly dirty hack: 
                                                                # if we need to redraw a component, we simply
                                                                # pick the component-definition from the template-source
                                                                # and parse it was a normal template
                                                                # this works! better than other ugly hacks!
        else:
            redraw_compo = None

        source, filename, uptodate = SmartAssetSpecLoader.get_source(self, environment, template)

        if redraw_compo:
            source = self.crop_compo_definiton(source, redraw_compo)
            if not source:
                raise TemplateNotFound, "Redraw-template for component '" + redraw_compo + "' in template '" + template + "'"

#        text_dict = epfli18n.get_text_dict()
#        keys = sorted([(len(key), key) for key in text_dict.keys()], reverse=True) # sorts all keys of the translation-dict by length in reverse order
#
#        for sort, txt in keys:
#            trans_txt = text_dict[txt]
#            source = source.replace("$" + txt, trans_txt) # because its ordered by length, no partial/wrong replacement can occur!

        return (source, filename, uptodate)

