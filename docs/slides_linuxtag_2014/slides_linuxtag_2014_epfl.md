# Building web tools - FAST!  <br> with <br> ![full_image](epfl-logo.png)

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
- ~ 35 mio offers and ~ 4 mio products from ~ 5000 shops
- matching and mapping of offers and products
- ~ 1 tb data processed on monthly basis
- stack:
	- python
	- postgresql / redis
	- apache
	- solr / elastic

---

# Why EPFL? <br> <sub> ... and yet another framework? </sub>

---

# Why EPFL?

There are many good other web frameworks!

But they tend to be very generalistic.

EPFL is very specialized on **form based web applications**.

This was exactly what we needed!

---

# Why EPFL?

This means:

- batteries included!
- fewer options (or: one way to do it right&trade;)!
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
- Access Control
- everything you really need to create form based web applications

---

# Why EPFL: fewer options!

- make good assumptions to fight complexity
- reduce options to keep maintainability
- **stop worrying and start coding!**

---

# Why EPFL: super powers!

- event based programming
- server side state
- no javascript programming

---

# what we have done

---

# EPFL

- *EPFL Python Frontend Logic*
<p>
- python
- pyramid-extension 
- only frontend logic:
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
        save_note = epfl.fields.Button(on_click = "save_note")


        def handle_save_note(self):
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
        delete_note = epfl.fields.Button(on_click = "delete_note")


        def handle_delete_note(self):
            self.show_confirm("Are you sure?", cmd_ok = "delete_confirmed")

        def handle_delete_confirmed(self):
            models.notes.delete_note(id = self.id.data)
            self.show_fading_message("The note has been deleted", "ok")



---

# server side state!

---

# Server side state

    !python
    ...
   
    def handle_add_tag(self):
        tag = self.tag.data
        self.page.parent.note_form.tags.append(tag)

- transactions to separate different units of work
- transactions can be nested
    - e.g. access previous pages (in wizards)
    - e.g. access parent page from an overlay-page

---

# no javascript coding!

---

# No javascript!

    !python

    # message
    self.show_fading_message("A nice message!", "ok")

    # check a value and do something
    if self.a_value.data == "good":
        self.page.jump(route_name = "route_name")
    else:
        self.page.jump(route_name = "other_route_name")



- every action in the browser is provided by the server-side (components)
    - show popup messages
    - button-actions depending on form values


---


# And now?

- more components
    - editable grid
    - tree
    - event-calendar
    - ...
- demo/example applications 
    - more pyramid scaffold templates
- a narrative documentation
    - e.g. how-to's

---

# And you?

- use it! (we do and so can you!)
- give feedback!
- get involved and improve it!

<div style="font-size:40px;text-align:center;margin-top:50px">
https://github.com/solute/pyramid_epfl
</div>

---

# Thank you!


---
# T-Shirt time!
---
# Category: EPFL
---
# What company started the EPFL?
---
# What language is EPFL written in?
---
# On which framework is EPFL based on?
---
# Which ORM is used?
---
# What are the super powers of EPFL?
---
# How many slides does this presentation have?
---

# Thank you! (again)


