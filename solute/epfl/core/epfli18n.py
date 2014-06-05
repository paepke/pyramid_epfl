#* encoding: utf-8

TRANSLATIONS = {"txt_value_required": "Bitte Wert eingeben!"}

class BasicDB(object):
    

    def gettext(self, msg):
        global TRANSLATIONS
        return TRANSLATIONS.get(msg, msg)
        
    def ngettext(self, singular, plural, n):
        if n == 1:
            return self.gettext(singular)
        else:
            return (plural)

