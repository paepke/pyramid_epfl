#* encoding: utf-8

TRANSLATIONS = {"txt_value_required": u"Bitte Wert eingeben!",
                "txt_upload_file_ok": u"Upload erfolgreich abgeschlossen.",
                "txt_upload_file_error": u"Fehler beim hochladen der Datei."}

class BasicDB(object):
    

    def gettext(self, msg):
        global TRANSLATIONS
        return TRANSLATIONS.get(msg, msg)
        
    def ngettext(self, singular, plural, n):
        if n == 1:
            return self.gettext(singular)
        else:
            return (plural)

