# Building thier tools - FAST!  <br> with <br> ![full_image](epfl-logo.png)

---

# self.about
- Gunter Bach
- 1974
- PET, ZX81, C64, PC
- Python since 1996 (1.4)
- Web-dev since 1998

---

# billiger.de
- full sortiment price comparison web platform
- ~ 1.5 mio products
- ~ 5000 shops
- ~ 1.2 tb data analysed on daily basis
- stack:
	- python
	- postgresql
	- apache
	- solr / elastic

---



# Why EPFL? <br> <sub> ... and yet another framework? </sub>

---

# Why EPFL?

There are many good other web frameworks!

But they tend to be very generalistic.

EPFL is very specialized on **form based web applications**.

---

# Why EPFL?

This means:

- batteries included!
- less options!
- super powers!


---

# Why EPFL: batteries included!

- rich set of components (really!)
	- forms (with rich set of widgets (really, really!!))
	- table (paginator, columns resizeable, sortable)
	- menu
	- tree
	- boxes (foldable)
	- ...
- ACL and users
- everything you really need to create form based web applications

---

# Why EPFL: less options!

- make good assumptions to fight complexity
- reduce options to keep maintainability
- stop worriying and start coding

---

# Why EPFL: super powers!

- event based programming
- server side state
- no javascript programming
- transactions

---

# what we have done

---

# EPFL

- python
- pyramid based (and others in the future)
- frontend logic:
	- only covers views
	- no ORM, authn, authz, ...
- few building blocks:
	- **pages**
	- **components**

---

# ...back to the super powers...

---

# events!

---


# Events

    !python
    class NoteForm(epfl.components.Form):
    
        ... field definition ...
        save_note = epfl.fields.Button(on_click = "SaveNote")


        def handle_SaveNote(self):
            if self.validate():
                data = self.get_data()
                models.notes.save_note(data)
                self.show_fading_message("The note has been saved", "ok")
            else:
                self.redraw()

---

# Events

    !python
    class NoteForm(epfl.components.Form):

        ... field definition ...
        delete_note = epfl.fields.Button(on_click = "DeleteNote")


        def handle_DeleteNote(self):
            self.show_confirm(u"Are you sure?", cmd_ok = "DeleteConfirmed")

        def handle_DeleteConfirmed(self):
            models.notes.delete_note(id = self.id.data)
            self.show_fading_message("The note has been deleted", "ok")



---

# server side state!

---

# Server side state

    !python
    ...
   
    def handle_AddTag(self):
        tag = self.tag.data
        self.page.parent.note_form.tags.append(tag)

---

# ... and transactions!

---

# Transactions

- store the state of a page
- fetch from db ![inline](pfeil.png) ![sub](pfeil_kreis.png) edit ![inline](pfeil.png) save to db
<br>
- can be nested

---

# Transactions

    !python
    ...

    def handle_AddTag(self):
        tag = self.tag.data
        self.page.parent.note_form.tags.append(tag)

---


# And now?

- more components
- more scaffold templates
- more documentation

---

# And you?

- use it!
- give feedback!
- improve it!

**https://github.com/solute/pyramid_epfl**

---

# Thank you!

