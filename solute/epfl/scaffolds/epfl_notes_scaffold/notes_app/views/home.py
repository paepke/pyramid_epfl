#* encoding: utf-8

import pyramid
from pyramid.view import view_config
from pyramid import security
from solute import epfl
import wtforms
import time

from notes_app import models


class NotesTable(epfl.components.Table):

    height = 100
    caption = "All notes"


    columns_def = [{"name": "icon_edit", "label": " ", "type": "icon", "sortable": False, "resizable": False,
                                    "default": {"src": "notes_app:static/edit_16x16.png", "tip": u"edit note"},
                                    "width": 20},
                   {"name": "id", "type": "id"},
                   {"name": "title", "label": "Title", "type": "text", "sortable": True, "resizable": True},
                   {"name": "note", "label": "Note", "type": "text", "sortable": True, "resizable": True},
                   ]

    on_row_click = "click_note"


    def getData(self, start_row, num_rows, sort_column, sort_order):

        total_count, rows = models.notes.get_notes(self.request, start_row, num_rows, sort_column, sort_order)

        for row in rows:
            if "\n" in row["note"]:
                row["note"] = row["note"][:row["note"].index("\n")] + "..."

        return total_count, rows


    def handle_click_note(self):

        self.page.note_form.load_note(id = self.getTargetRowId())


class TagsTable(epfl.components.Table):

    height = 200
    caption = "All tags"


    columns_def = [{"name": "icon_delete", "label": " ", "type": "icon", "sortable": False, "resizable": False,
                                    "default": {"src": "notes_app:static/delete_16x16.png", 
                                                "tip": u"delete tag",
                                                "cmd": "delete_tag"},
                                    "width": 20},
                   {"name": "id", "type": "id"},
                   {"name": "tag", "label": "Tag", "type": "text", "sortable": True, "resizable": True},
                   ]

    on_row_click = "click_tag"


    def getData(self, start_row, num_rows, sort_column, sort_order):
        total_count, rows = models.tags.get_tags(self.request, start_row, num_rows, sort_column, sort_order)
        return total_count, rows


    def handle_click_tag(self):
        id = self.getTargetRowId()
        tag = models.tags.get_tag(self.request, id)
        old_tags = self.page.parent.note_form.tags.data.strip()
        if old_tags:
            new_tags = old_tags + ", " + tag["tag"]
        else:
            new_tags = tag["tag"]
        self.page.parent.note_form.tags.data = new_tags
        self.page.parent.note_form.redraw()
        
        self.page.close_overlay()

    def handle_delete_tag(self):

        models.tags.delete_tag(self.request, id = self.getTargetRowId())
        self.refresh_data()



class NoteForm(epfl.components.Form):

    title = epfl.fields.Entry("Title", 
                              type = "char(32)", 
                              default = "A note", 
                              description = u"This this is note title!",
                              mandatory = True)
    note = epfl.fields.TextArea("Note", mandatory = True)
    tags = epfl.fields.Entry("Tags",
                             type = "char(128)",
                             description = "A comma separated list of tags for this note")

    save = epfl.fields.Button(on_click = "save_note")
    delete = epfl.fields.Button(on_click = "delete_note")
    new = epfl.fields.Button(on_click = "new_note")
    add_tag = epfl.fields.Button(on_click = "add_tag")

    def handle_save_note(self):

        if self.validate():
            data = self.get_data()

            if "id" not in data:
                new_id = models.notes.create_note(self.request, data)
                self.set_data({"id": new_id})
                self.show_fading_message("Note has been created!", "ok")
            else:
                models.notes.save_note(self.request, data)
                self.show_fading_message("Note has been saved.", "ok")

            self.page.notes_table.refresh_data()

        self.redraw()


    def handle_new_note(self):

        self.reset_data(additional_data = True)        
        self.redraw()

    def handle_delete_note(self):
        note_id = self.get_data().get("id")
        if not note_id:
            self.show_fading_message("Please select a note first!", "error")
        else:
            self.show_confirm(u"Are you sure?", cmd_ok = "delete_note_confirmed")

    def handle_delete_note_confirmed(self):

        note_id = self.get_data().get("id")
        models.notes.delete_note(self.request, note_id)
        self.page.notes_table.refresh_data()
        self.handle_new_note()

    def handle_add_tag(self):
        self.page.open_overlay(route = "tags_selector")


    def load_note(self, id):

        data = models.notes.get_note(self.request, id)
        self.set_data(data)
        self.redraw()


class TagsForm(epfl.components.Form):

    new_tag = epfl.fields.Entry("Title", 
                                type = "char(32)", 
                                mandatory = True)
    add_tag = epfl.fields.Button(label = "Create Tag", on_click = "add_tag")


    def handle_add_tag(self):

        if self.validate():
            models.tags.create_tag(self.request, {"tag": self.new_tag.data})
            self.new_tag.reset_data()
            self.page.tags_table.refresh_data()

        self.redraw()            



# --- PAGES ----


@view_config(route_name = 'home')
class HomePage(epfl.Page):

    template = "home.html"

    def setup_components(self):

        self.notes_table = NotesTable()
        self.note_form = NoteForm()

@view_config(route_name = "tags_selector")
class TagsSelectorPage(epfl.Page):

    template = "tags_selector.html"

    def setup_components(self):

        self.tags_table = TagsTable()
        self.tags_form = TagsForm()



def includeme(config):
    config.add_route('home', '/')    
    config.add_route("tags_selector", "/select_tags")


