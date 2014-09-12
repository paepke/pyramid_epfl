#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl
import time, datetime

DUMMY_ID = 1

class DummyCompo(epfl.components.Canvas):

    template_name = "dummy_compo.html"
    compo_state = ["dummy_id"]

    dummy_id = "no state"

    def init_transaction(self):
        global DUMMY_ID

        self.dummy_id = DUMMY_ID

        DUMMY_ID += 1

    def handle_close(self):

        self.delete_component()
        self.page.box.redraw()

class Foermchen(epfl.components.Form):

    remove = epfl.fields.Button(on_click = "remove")
    save = epfl.fields.Button(on_click = "save")

    def handle_save(self):
        print "YO, saving form", self.cid, self.get_data()

    def handle_remove(self):
        self.delete_component()
        self.page.box.redraw()

class Form(epfl.components.Form):
    

    add = epfl.fields.Button(on_click = "add")
    reload = epfl.fields.Button(on_click = "reload")


    def handle_add(self):
        fields = [epfl.fields.Entry(id = "a_entry", label = "Eingabefeld 1"),
                  epfl.fields.Select(id = "a_select", label = "Auswahl", choices = [("a", "Ah"), ("b", "Beh"), ("c", "Zeh!")])]
        compo = Foermchen.with_dynamic_fields(fields)
        self.page.box.add_component(compo)
        self.page.box.redraw()

    def handle_reload(self):
        self.page.box.redraw()



@view_config(route_name='home')
class HomePage(epfl.Page):

    template = "home.html"

    def setup_components(self):

        self.box = epfl.components.Box()        
        self.form = Form()



