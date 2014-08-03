How to make forms dynamic
=========================

Dynamic forms in EPFL are very similar to dynamic forms in wtforms (since we are using wtforms as the base of the form component this should not be a big surprise!).
Also the restrictions come from there. So you do not have "truly" dynamic forms but you can decide on creation time (of the form component) which fields/widgets the form has. The difference to a truly dynamic form is, that you can not change (add or remove fields) a form-component once it is created. Of course every dynamically created form behaves just as a normal one. In fact there is not much difference between them.

A dynamic form starts with a "bootstrap" form-component-class:


	.. code:: python

		class Foermchen(epfl.components.Form):

    		save = epfl.fields.Button(on_click = "save")

		    def handle_save(self):
        		print "saving form", self.get_data()

There also all event-handlers must be coded. Right now there is no way to add dynamically event-handlers or data-source-functions.
The bootstrap-form contains the fields common to all the dynamically created forms. It can be also a complete empty subinstance of "epfl.component.Form".

Once you have your bootstrap-form-class ready you can instanciate it like this:

	.. code:: python


	    def handle_add(self):

	    	# we define some fields to add to "Foermchen"-Form-Bootstrap-Class:

    	    fields = [epfl.fields.Entry(id = "a_entry", label = "Eingabefeld 1"),
        	          epfl.fields.Select(id = "a_select", label = "Auswahl", choices = [("a", "Ah"), ("b", "Beh"), ("c", "Zeh!")])]

        	# we use the Class Foermchen:
       	 	compo = Foermchen.with_dynamic_fields(fields)

       	 	# then we add it to a "box"-container-component
       	 	self.page.box.add_component(compo)

       	 	# don't forget to redraw the box
        	self.page.box.redraw()

In this scenario we have some other component that has an event "add". This creates dyamically - in this case a fixed list of two fields - a form component derived from the bootstrap-form "Foermchen". Of course you could create the fields by some other mechanism like from some description taken from a database. The form-component-object (called "compo" here) behaves exactly like any other form.





